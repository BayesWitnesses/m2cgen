import json
import math
import numpy as np

from m2cgen import ast
from m2cgen.assemblers import fallback_expressions, utils
from m2cgen.assemblers.base import ModelAssembler
from m2cgen.assemblers.linear import _linear_to_ast


class BaseBoostingAssembler(ModelAssembler):

    classifier_names = {}
    multiclass_params_seq_len = 1

    def __init__(self, model, estimator_params, base_score=0.0):
        super().__init__(model)
        self._all_estimator_params = estimator_params
        self._base_score = base_score

        self._output_size = 1
        self._is_classification = False

        model_class_name = type(model).__name__
        if model_class_name in self.classifier_names:
            self._is_classification = True
            if model.n_classes_ > 2:
                self._output_size = model.n_classes_

    def assemble(self):
        if self._is_classification:
            if self._output_size == 1:
                return self._assemble_bin_class_output(
                    self._all_estimator_params)
            else:
                return self._assemble_multi_class_output(
                    self._all_estimator_params)
        else:
            result_ast = self._assemble_single_output(
                self._all_estimator_params, base_score=self._base_score)
            return self._single_convert_output(result_ast)

    def _assemble_single_output(self, estimator_params,
                                base_score=0.0, split_idx=0):
        estimators_ast = self._assemble_estimators(estimator_params, split_idx)

        tmp_ast = utils.apply_op_to_expressions(
            ast.BinNumOpType.ADD,
            *estimators_ast)

        if base_score != 0.0:
            tmp_ast = utils.apply_bin_op(
                ast.NumVal(base_score),
                tmp_ast,
                ast.BinNumOpType.ADD)

        result_ast = self._final_transform(tmp_ast)

        return result_ast

    def _assemble_multi_class_output(self, estimator_params):
        # Multi-class output is calculated based on discussion in
        # https://github.com/dmlc/xgboost/issues/1746#issuecomment-295962863
        # and the enhancement to support boosted forests in XGBoost.
        splits = _split_estimator_params_by_classes(
            estimator_params, self._output_size,
            self.multiclass_params_seq_len)

        base_score = self._base_score
        exprs = [
            self._assemble_single_output(e, base_score=base_score, split_idx=i)
            for i, e in enumerate(splits)
        ]

        proba_exprs = self._multi_class_convert_output(exprs)
        return ast.VectorVal(proba_exprs)

    def _assemble_bin_class_output(self, estimator_params):
        # Base score is calculated based on
        # https://github.com/dmlc/xgboost/blob/8de7f1928e4815843fbf8773a5ac7ecbc37b2e15/src/objective/regression_loss.h#L91
        # return -logf(1.0f / base_score - 1.0f);
        base_score = 0.0
        if self._base_score != 0.0:
            base_score = -math.log(1.0 / self._base_score - 1.0)

        expr = self._assemble_single_output(
            estimator_params, base_score=base_score)

        proba_expr = self._bin_class_convert_output(expr)

        return ast.VectorVal([
            ast.BinNumExpr(ast.NumVal(1.0), proba_expr, ast.BinNumOpType.SUB),
            proba_expr
        ])

    def _final_transform(self, ast_to_transform):
        return ast_to_transform

    def _multi_class_convert_output(self, exprs):
        return fallback_expressions.softmax(exprs)

    def _bin_class_convert_output(self, expr, to_reuse=True):
        return fallback_expressions.sigmoid(expr, to_reuse=to_reuse)

    def _single_convert_output(self, expr):
        return expr

    def _assemble_estimators(self, estimator_params, split_idx):
        raise NotImplementedError


class BaseTreeBoostingAssembler(BaseBoostingAssembler):

    def __init__(self, model, trees, base_score=0.0, tree_limit=None):
        super().__init__(model, trees, base_score=base_score)
        assert tree_limit is None or tree_limit > 0, "Unexpected tree limit"
        self._tree_limit = tree_limit

    def _assemble_estimators(self, trees, split_idx):
        if self._tree_limit:
            trees = trees[:self._tree_limit]

        return [self._assemble_tree(t) for t in trees]

    def _assemble_tree(self, tree):
        raise NotImplementedError


class XGBoostTreeModelAssembler(BaseTreeBoostingAssembler):

    classifier_names = {"XGBClassifier", "XGBRFClassifier"}

    def __init__(self, model):
        self.multiclass_params_seq_len = model.get_params().get(
            "num_parallel_tree", 1)
        feature_names = model.get_booster().feature_names
        self._feature_name_to_idx = {
            name: idx for idx, name in enumerate(feature_names or [])
        }

        model_dump = model.get_booster().get_dump(dump_format="json")
        trees = [json.loads(d) for d in model_dump]

        # Limit the number of trees that should be used for
        # assembling (if applicable).
        best_ntree_limit = getattr(model, "best_ntree_limit", None)

        super().__init__(model, trees,
                         base_score=model.get_params()["base_score"],
                         tree_limit=best_ntree_limit)

    def _assemble_tree(self, tree):
        if "leaf" in tree:
            return ast.NumVal(tree["leaf"], dtype=np.float32)

        threshold = ast.NumVal(tree["split_condition"], dtype=np.float32)
        split = tree["split"]
        feature_idx = self._feature_name_to_idx.get(split, split)
        feature_ref = ast.FeatureRef(feature_idx)

        # Since comparison with NaN (missing) value always returns false we
        # should make sure that the node ID specified in the "missing" field
        # always ends up in the "else" branch of the ast.IfExpr.
        use_lt_comp = tree["missing"] == tree["no"]
        if use_lt_comp:
            comp_op = ast.CompOpType.LT
            true_child_id = tree["yes"]
            false_child_id = tree["no"]
        else:
            comp_op = ast.CompOpType.GTE
            true_child_id = tree["no"]
            false_child_id = tree["yes"]

        return ast.IfExpr(ast.CompExpr(feature_ref, threshold, comp_op),
                          self._assemble_child_tree(tree, true_child_id),
                          self._assemble_child_tree(tree, false_child_id))

    def _assemble_child_tree(self, tree, child_id):
        for child in tree["children"]:
            if child["nodeid"] == child_id:
                return self._assemble_tree(child)
        assert False, f"Unexpected child ID: {child_id}"


class XGBoostLinearModelAssembler(BaseBoostingAssembler):

    classifier_names = {"XGBClassifier"}

    def __init__(self, model):
        model_dump = model.get_booster().get_dump(dump_format="json")
        weights = json.loads(model_dump[0])["weight"]
        self._bias = json.loads(model_dump[0])["bias"]
        super().__init__(model, weights,
                         base_score=model.get_params()["base_score"])

    def _assemble_estimators(self, weights, split_idx):
        coef = utils.to_1d_array(weights)
        return [_linear_to_ast(coef, self._bias[split_idx])]


class XGBoostModelAssemblerSelector(ModelAssembler):

    def __init__(self, model, *args, **kwargs):
        model_dump = model.get_booster().get_dump(dump_format="json")
        if len(model_dump) == 1 and all(i in json.loads(model_dump[0])
                                        for i in ("weight", "bias")):
            self.assembler = XGBoostLinearModelAssembler(model)
        else:
            self.assembler = XGBoostTreeModelAssembler(model, *args, **kwargs)

    def assemble(self):
        return self.assembler.assemble()


class LightGBMModelAssembler(BaseTreeBoostingAssembler):

    classifier_names = {"LGBMClassifier"}

    def __init__(self, model):
        model_dump = model.booster_.dump_model()
        trees = [m["tree_structure"] for m in model_dump["tree_info"]]

        self.n_iter = len(trees) // model_dump["num_tree_per_iteration"]
        self.average_output = model_dump.get("average_output", False)
        self.objective_config_parts = model_dump.get(
            "objective", "custom").split(" ")
        self.objective_name = self.objective_config_parts[0]

        super().__init__(model, trees)

    def _final_transform(self, ast_to_transform):
        if self.average_output:
            coef = 1 / self.n_iter
            return utils.apply_bin_op(
                ast_to_transform,
                ast.NumVal(coef),
                ast.BinNumOpType.MUL)
        else:
            return super()._final_transform(ast_to_transform)

    def _multi_class_convert_output(self, exprs):
        supported_objectives = {
            "multiclass": super()._multi_class_convert_output,
            "multiclassova": self._multi_class_sigmoid_transform,
            "custom": super()._single_convert_output,
        }
        if self.objective_name not in supported_objectives:
            raise ValueError(
                f"Unsupported objective function '{self.objective_name}'")
        return supported_objectives[self.objective_name](exprs)

    def _multi_class_sigmoid_transform(self, exprs):
        return [self._bin_class_sigmoid_transform(expr, to_reuse=False)
                for expr in exprs]

    def _bin_class_convert_output(self, expr, to_reuse=True):
        supported_objectives = {
            "binary": self._bin_class_sigmoid_transform,
            "custom": super()._single_convert_output,
        }
        if self.objective_name not in supported_objectives:
            raise ValueError(
                f"Unsupported objective function '{self.objective_name}'")
        return supported_objectives[self.objective_name](expr)

    def _bin_class_sigmoid_transform(self, expr, to_reuse=True):
        coef = 1.0
        for config_part in self.objective_config_parts:
            config_entry = config_part.split(":")
            if config_entry[0] == "sigmoid":
                coef = np.float64(config_entry[1])
                break
        return super()._bin_class_convert_output(
            utils.mul(ast.NumVal(coef), expr) if coef != 1.0 else expr,
            to_reuse=to_reuse)

    def _single_convert_output(self, expr):
        supported_objectives = {
            "cross_entropy": fallback_expressions.sigmoid,
            "cross_entropy_lambda": self._log1p_exp_transform,
            "regression": self._maybe_sqr_transform,
            "regression_l1": self._maybe_sqr_transform,
            "huber": super()._single_convert_output,
            "fair": self._maybe_sqr_transform,
            "poisson": self._exp_transform,
            "quantile": self._maybe_sqr_transform,
            "mape": self._maybe_sqr_transform,
            "gamma": self._exp_transform,
            "tweedie": self._exp_transform,
            "custom": super()._single_convert_output,
        }
        if self.objective_name not in supported_objectives:
            raise ValueError(
                f"Unsupported objective function '{self.objective_name}'")
        return supported_objectives[self.objective_name](expr)

    def _log1p_exp_transform(self, expr):
        return ast.Log1pExpr(ast.ExpExpr(expr))

    def _maybe_sqr_transform(self, expr):
        if "sqrt" in self.objective_config_parts:
            expr = ast.IdExpr(expr, to_reuse=True)
            return utils.mul(ast.AbsExpr(expr), expr)
        else:
            return expr

    def _exp_transform(self, expr):
        return ast.ExpExpr(expr)

    def _assemble_tree(self, tree):
        if "leaf_value" in tree:
            return ast.NumVal(tree["leaf_value"])

        threshold = ast.NumVal(tree["threshold"])
        feature_ref = ast.FeatureRef(tree["split_feature"])

        op = ast.CompOpType.from_str_op(tree["decision_type"])
        assert op == ast.CompOpType.LTE, "Unexpected comparison op"

        missing_type = tree['missing_type']

        if missing_type not in {"NaN", "None"}:
            raise ValueError(f"Unknown missing_type: {missing_type}")

        reverse_condition = missing_type == "NaN" and tree["default_left"]
        reverse_condition |= missing_type == "None" and tree["threshold"] >= 0
        if reverse_condition:
            op = ast.CompOpType.GT
            true_child = tree["right_child"]
            false_child = tree["left_child"]
        else:
            true_child = tree["left_child"]
            false_child = tree["right_child"]

        return ast.IfExpr(
            ast.CompExpr(feature_ref, threshold, op),
            self._assemble_tree(true_child),
            self._assemble_tree(false_child))


def _split_estimator_params_by_classes(values, n_classes, params_seq_len):
    # Splits are computed based on a comment
    # https://github.com/dmlc/xgboost/issues/1746#issuecomment-267400592
    # and the enhancement to support boosted forests in XGBoost.
    values_len = len(values)
    block_len = n_classes * params_seq_len
    indices = list(range(values_len))
    indices_by_class = np.array(
        [[indices[i:i + params_seq_len]
          for i in range(j, values_len, block_len)]
         for j in range(0, block_len, params_seq_len)]
        ).reshape(n_classes, -1)
    return [[values[idx] for idx in class_idxs]
            for class_idxs in indices_by_class]
