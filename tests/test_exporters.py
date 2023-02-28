from m2cgen import exporters


def test_export_to_java(trained_model):
    generated_code = exporters.export_to_java(trained_model).strip()
    assert generated_code.startswith("""
public class Model {
    public static double score(double[] input) {
        return
""".strip())


def test_export_to_python(trained_model):
    generated_code = exporters.export_to_python(trained_model).strip()
    assert generated_code.startswith("""
def score(input):
    return
""".strip())


def test_export_to_c(trained_model):
    generated_code = exporters.export_to_c(trained_model).strip()
    assert generated_code.startswith("""
double score(double * input) {
    return
""".strip())


def test_export_to_go(trained_model):
    generated_code = exporters.export_to_go(trained_model).strip()
    assert generated_code.startswith("""
func score(input []float64) float64 {
    return
""".strip())


def test_export_to_javascript(trained_model):
    generated_code = exporters.export_to_javascript(trained_model).strip()
    assert generated_code.startswith("""
function score(input) {
    return
""".strip())


def test_export_to_visual_basic(trained_model):
    generated_code = exporters.export_to_visual_basic(trained_model).strip()
    assert generated_code.startswith("""
Module Model
Function Score(ByRef inputVector() As Double) As Double
    Score =
""".strip())


def test_export_to_c_sharp(trained_model):
    generated_code = exporters.export_to_c_sharp(trained_model).strip()
    assert generated_code.startswith("""
namespace ML {
    public static class Model {
        public static double Score(double[] input) {
            return
""".strip())


def test_export_to_powershell(trained_model):
    generated_code = exporters.export_to_powershell(trained_model).strip()
    assert generated_code.startswith("""
function Score([double[]] $InputVector) {
    return
""".strip())


def test_export_to_r(trained_model):
    generated_code = exporters.export_to_r(trained_model).strip()
    assert generated_code.startswith("""
score <- function(input) {
    return(
""".strip())


def test_export_to_php(trained_model):
    generated_code = exporters.export_to_php(trained_model).strip()
    assert generated_code.startswith("""
<?php
function score(array $input) {
    return
""".strip())


def test_export_to_dart(trained_model):
    generated_code = exporters.export_to_dart(trained_model).strip()
    assert generated_code.startswith("""
double score(List<double> input) {
    return
""".strip())


def test_export_to_haskell(trained_model):
    generated_code = exporters.export_to_haskell(trained_model).strip()
    assert generated_code.startswith("""
module Model where
score :: [Double] -> Double
score input =
""".strip())


def test_export_to_ruby(trained_model):
    generated_code = exporters.export_to_ruby(trained_model).strip()
    assert generated_code.startswith("""
def score(input)
""".strip())


def test_export_to_f_sharp(trained_model):
    generated_code = exporters.export_to_f_sharp(trained_model).strip()
    assert generated_code.startswith("""
let score (input : double list) =
""".strip())


def test_export_to_rust(trained_model):
    generated_code = exporters.export_to_rust(trained_model).strip()
    assert generated_code.startswith("""
fn score(input: Vec<f64>) -> f64 {
""".strip())


def test_export_to_fortran(trained_model):
    generated_code = exporters.export_to_fortran(trained_model).strip()
    assert generated_code.startswith("""
function score(input)
    double precision :: score
    double precision, dimension(:) :: input
""".strip())
