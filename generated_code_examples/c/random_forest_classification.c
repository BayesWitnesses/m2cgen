void assign_array(double source[], double *target, int size) {
    for(int i = 0; i < size; ++i)
        target[i] = source[i];
}
void add_vectors(double *v1, double *v2, int size, double *result) {
    for(int i = 0; i < size; ++i)
        result[i] = v1[i] + v2[i];
}
void mul_vector_number(double *v1, double num, int size, double *result) {
    for(int i = 0; i < size; ++i)
        result[i] = v1[i] * num;
}
void score(double * input, double * output) {
    double var0[3];
    double var1[3];
    double var2[3];
    double var3[3];
    double var4[3];
    double var5[3];
    double var6[3];
    double var7[3];
    double var8[3];
    double var9[3];
    double var10[3];
    if ((input[3]) <= (0.8)) {
        assign_array((double[]){1.0, 0.0, 0.0}, var10, 3);
    } else {
        if ((input[2]) <= (4.8500004)) {
            if ((input[1]) <= (2.55)) {
                if ((input[3]) <= (1.6)) {
                    assign_array((double[]){0.0, 1.0, 0.0}, var10, 3);
                } else {
                    assign_array((double[]){0.0, 0.0, 1.0}, var10, 3);
                }
            } else {
                assign_array((double[]){0.0, 1.0, 0.0}, var10, 3);
            }
        } else {
            if ((input[3]) <= (1.75)) {
                if ((input[0]) <= (6.95)) {
                    if ((input[3]) <= (1.55)) {
                        if ((input[2]) <= (4.95)) {
                            assign_array((double[]){0.0, 1.0, 0.0}, var10, 3);
                        } else {
                            assign_array((double[]){0.0, 0.0, 1.0}, var10, 3);
                        }
                    } else {
                        assign_array((double[]){0.0, 1.0, 0.0}, var10, 3);
                    }
                } else {
                    assign_array((double[]){0.0, 0.0, 1.0}, var10, 3);
                }
            } else {
                assign_array((double[]){0.0, 0.0, 1.0}, var10, 3);
            }
        }
    }
    mul_vector_number(var10, 0.1, 3, var9);
    double var11[3];
    double var12[3];
    if ((input[3]) <= (0.8)) {
        assign_array((double[]){1.0, 0.0, 0.0}, var12, 3);
    } else {
        if ((input[0]) <= (6.05)) {
            if ((input[2]) <= (4.9)) {
                if ((input[0]) <= (4.95)) {
                    assign_array((double[]){0.0, 0.0, 1.0}, var12, 3);
                } else {
                    assign_array((double[]){0.0, 1.0, 0.0}, var12, 3);
                }
            } else {
                assign_array((double[]){0.0, 0.0, 1.0}, var12, 3);
            }
        } else {
            if ((input[3]) <= (1.75)) {
                if ((input[1]) <= (3.05)) {
                    if ((input[2]) <= (5.05)) {
                        assign_array((double[]){0.0, 1.0, 0.0}, var12, 3);
                    } else {
                        assign_array((double[]){0.0, 0.0, 1.0}, var12, 3);
                    }
                } else {
                    assign_array((double[]){0.0, 1.0, 0.0}, var12, 3);
                }
            } else {
                assign_array((double[]){0.0, 0.0, 1.0}, var12, 3);
            }
        }
    }
    mul_vector_number(var12, 0.1, 3, var11);
    add_vectors(var9, var11, 3, var8);
    double var13[3];
    double var14[3];
    if ((input[2]) <= (2.6)) {
        assign_array((double[]){1.0, 0.0, 0.0}, var14, 3);
    } else {
        if ((input[3]) <= (1.75)) {
            if ((input[2]) <= (5.05)) {
                assign_array((double[]){0.0, 1.0, 0.0}, var14, 3);
            } else {
                if ((input[2]) <= (5.35)) {
                    if ((input[1]) <= (2.75)) {
                        assign_array((double[]){0.0, 1.0, 0.0}, var14, 3);
                    } else {
                        assign_array((double[]){0.0, 0.0, 1.0}, var14, 3);
                    }
                } else {
                    assign_array((double[]){0.0, 0.0, 1.0}, var14, 3);
                }
            }
        } else {
            assign_array((double[]){0.0, 0.0, 1.0}, var14, 3);
        }
    }
    mul_vector_number(var14, 0.1, 3, var13);
    add_vectors(var8, var13, 3, var7);
    double var15[3];
    double var16[3];
    if ((input[3]) <= (0.7)) {
        assign_array((double[]){1.0, 0.0, 0.0}, var16, 3);
    } else {
        if ((input[2]) <= (4.8500004)) {
            if ((input[3]) <= (1.6500001)) {
                assign_array((double[]){0.0, 1.0, 0.0}, var16, 3);
            } else {
                if ((input[1]) <= (2.85)) {
                    assign_array((double[]){0.0, 0.0, 1.0}, var16, 3);
                } else {
                    assign_array((double[]){0.0, 1.0, 0.0}, var16, 3);
                }
            }
        } else {
            if ((input[3]) <= (1.75)) {
                if ((input[0]) <= (6.2)) {
                    if ((input[1]) <= (2.65)) {
                        assign_array((double[]){0.0, 0.0, 1.0}, var16, 3);
                    } else {
                        assign_array((double[]){0.0, 1.0, 0.0}, var16, 3);
                    }
                } else {
                    assign_array((double[]){0.0, 1.0, 0.0}, var16, 3);
                }
            } else {
                assign_array((double[]){0.0, 0.0, 1.0}, var16, 3);
            }
        }
    }
    mul_vector_number(var16, 0.1, 3, var15);
    add_vectors(var7, var15, 3, var6);
    double var17[3];
    double var18[3];
    if ((input[3]) <= (0.7)) {
        assign_array((double[]){1.0, 0.0, 0.0}, var18, 3);
    } else {
        if ((input[3]) <= (1.6500001)) {
            if ((input[3]) <= (1.55)) {
                if ((input[1]) <= (2.65)) {
                    if ((input[3]) <= (1.3499999)) {
                        assign_array((double[]){0.0, 1.0, 0.0}, var18, 3);
                    } else {
                        if ((input[0]) <= (6.2)) {
                            assign_array((double[]){0.0, 0.0, 1.0}, var18, 3);
                        } else {
                            assign_array((double[]){0.0, 1.0, 0.0}, var18, 3);
                        }
                    }
                } else {
                    assign_array((double[]){0.0, 1.0, 0.0}, var18, 3);
                }
            } else {
                if ((input[2]) <= (5.45)) {
                    assign_array((double[]){0.0, 1.0, 0.0}, var18, 3);
                } else {
                    assign_array((double[]){0.0, 0.0, 1.0}, var18, 3);
                }
            }
        } else {
            assign_array((double[]){0.0, 0.0, 1.0}, var18, 3);
        }
    }
    mul_vector_number(var18, 0.1, 3, var17);
    add_vectors(var6, var17, 3, var5);
    double var19[3];
    double var20[3];
    if ((input[3]) <= (0.75)) {
        assign_array((double[]){1.0, 0.0, 0.0}, var20, 3);
    } else {
        if ((input[3]) <= (1.75)) {
            if ((input[3]) <= (1.3499999)) {
                assign_array((double[]){0.0, 1.0, 0.0}, var20, 3);
            } else {
                if ((input[2]) <= (5.05)) {
                    if ((input[1]) <= (2.65)) {
                        if ((input[2]) <= (4.7)) {
                            assign_array((double[]){0.0, 0.0, 1.0}, var20, 3);
                        } else {
                            if ((input[2]) <= (4.95)) {
                                assign_array((double[]){0.0, 1.0, 0.0}, var20, 3);
                            } else {
                                assign_array((double[]){0.0, 0.0, 1.0}, var20, 3);
                            }
                        }
                    } else {
                        assign_array((double[]){0.0, 1.0, 0.0}, var20, 3);
                    }
                } else {
                    assign_array((double[]){0.0, 0.0, 1.0}, var20, 3);
                }
            }
        } else {
            assign_array((double[]){0.0, 0.0, 1.0}, var20, 3);
        }
    }
    mul_vector_number(var20, 0.1, 3, var19);
    add_vectors(var5, var19, 3, var4);
    double var21[3];
    double var22[3];
    if ((input[2]) <= (2.7)) {
        assign_array((double[]){1.0, 0.0, 0.0}, var22, 3);
    } else {
        if ((input[3]) <= (1.75)) {
            if ((input[0]) <= (7.0)) {
                if ((input[2]) <= (4.9)) {
                    assign_array((double[]){0.0, 1.0, 0.0}, var22, 3);
                } else {
                    if ((input[1]) <= (2.65)) {
                        assign_array((double[]){0.0, 0.0, 1.0}, var22, 3);
                    } else {
                        if ((input[3]) <= (1.55)) {
                            assign_array((double[]){0.0, 0.0, 1.0}, var22, 3);
                        } else {
                            assign_array((double[]){0.0, 1.0, 0.0}, var22, 3);
                        }
                    }
                }
            } else {
                assign_array((double[]){0.0, 0.0, 1.0}, var22, 3);
            }
        } else {
            if ((input[2]) <= (4.8500004)) {
                if ((input[0]) <= (5.95)) {
                    assign_array((double[]){0.0, 1.0, 0.0}, var22, 3);
                } else {
                    assign_array((double[]){0.0, 0.0, 1.0}, var22, 3);
                }
            } else {
                assign_array((double[]){0.0, 0.0, 1.0}, var22, 3);
            }
        }
    }
    mul_vector_number(var22, 0.1, 3, var21);
    add_vectors(var4, var21, 3, var3);
    double var23[3];
    double var24[3];
    if ((input[3]) <= (0.8)) {
        assign_array((double[]){1.0, 0.0, 0.0}, var24, 3);
    } else {
        if ((input[2]) <= (4.8500004)) {
            assign_array((double[]){0.0, 1.0, 0.0}, var24, 3);
        } else {
            if ((input[2]) <= (5.2)) {
                if ((input[0]) <= (6.5)) {
                    if ((input[2]) <= (5.05)) {
                        assign_array((double[]){0.0, 0.0, 1.0}, var24, 3);
                    } else {
                        if ((input[1]) <= (2.75)) {
                            if ((input[0]) <= (5.9)) {
                                assign_array((double[]){0.0, 0.0, 1.0}, var24, 3);
                            } else {
                                assign_array((double[]){0.0, 1.0, 0.0}, var24, 3);
                            }
                        } else {
                            assign_array((double[]){0.0, 0.0, 1.0}, var24, 3);
                        }
                    }
                } else {
                    if ((input[1]) <= (3.05)) {
                        assign_array((double[]){0.0, 1.0, 0.0}, var24, 3);
                    } else {
                        assign_array((double[]){0.0, 0.0, 1.0}, var24, 3);
                    }
                }
            } else {
                assign_array((double[]){0.0, 0.0, 1.0}, var24, 3);
            }
        }
    }
    mul_vector_number(var24, 0.1, 3, var23);
    add_vectors(var3, var23, 3, var2);
    double var25[3];
    double var26[3];
    if ((input[2]) <= (4.8500004)) {
        if ((input[0]) <= (5.45)) {
            if ((input[3]) <= (0.8)) {
                assign_array((double[]){1.0, 0.0, 0.0}, var26, 3);
            } else {
                assign_array((double[]){0.0, 1.0, 0.0}, var26, 3);
            }
        } else {
            assign_array((double[]){0.0, 1.0, 0.0}, var26, 3);
        }
    } else {
        if ((input[3]) <= (1.75)) {
            if ((input[2]) <= (5.3)) {
                if ((input[0]) <= (6.15)) {
                    assign_array((double[]){0.0, 0.0, 1.0}, var26, 3);
                } else {
                    assign_array((double[]){0.0, 1.0, 0.0}, var26, 3);
                }
            } else {
                assign_array((double[]){0.0, 0.0, 1.0}, var26, 3);
            }
        } else {
            assign_array((double[]){0.0, 0.0, 1.0}, var26, 3);
        }
    }
    mul_vector_number(var26, 0.1, 3, var25);
    add_vectors(var2, var25, 3, var1);
    double var27[3];
    double var28[3];
    if ((input[2]) <= (2.6)) {
        assign_array((double[]){1.0, 0.0, 0.0}, var28, 3);
    } else {
        if ((input[2]) <= (4.8500004)) {
            if ((input[3]) <= (1.6500001)) {
                assign_array((double[]){0.0, 1.0, 0.0}, var28, 3);
            } else {
                if ((input[3]) <= (1.75)) {
                    assign_array((double[]){0.0, 0.0, 1.0}, var28, 3);
                } else {
                    assign_array((double[]){0.0, 1.0, 0.0}, var28, 3);
                }
            }
        } else {
            if ((input[1]) <= (2.75)) {
                if ((input[3]) <= (1.7)) {
                    if ((input[3]) <= (1.55)) {
                        if ((input[2]) <= (4.95)) {
                            assign_array((double[]){0.0, 1.0, 0.0}, var28, 3);
                        } else {
                            assign_array((double[]){0.0, 0.0, 1.0}, var28, 3);
                        }
                    } else {
                        assign_array((double[]){0.0, 1.0, 0.0}, var28, 3);
                    }
                } else {
                    assign_array((double[]){0.0, 0.0, 1.0}, var28, 3);
                }
            } else {
                assign_array((double[]){0.0, 0.0, 1.0}, var28, 3);
            }
        }
    }
    mul_vector_number(var28, 0.1, 3, var27);
    add_vectors(var1, var27, 3, var0);
    assign_array(var0, output, 3);
}
