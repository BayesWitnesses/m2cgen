#include <math.h>
void assign_array(double source[], double *target, int size) {
    for(int i = 0; i < size; ++i)
        target[i] = source[i];
}
void score(double * input, double * output) {
    double var0;
    if ((input[2]) <= (1.8)) {
        var0 = -0.9486122853153485;
    } else {
        if ((input[2]) <= (4.250000000000001)) {
            var0 = -1.1633850173886202;
        } else {
            var0 = -1.1736122903444903;
        }
    }
    double var1;
    if ((input[2]) <= (1.8)) {
        var1 = 0.12984943093573026;
    } else {
        if ((input[1]) <= (3.0500000000000003)) {
            if ((input[2]) <= (4.250000000000001)) {
                var1 = -0.07260616006169109;
            } else {
                if ((input[1]) <= (2.85)) {
                    var1 = -0.0721999366682237;
                } else {
                    var1 = -0.07223800798778846;
                }
            }
        } else {
            var1 = -0.06203500259944528;
        }
    }
    double var2;
    if ((input[2]) <= (1.8)) {
        var2 = 0.11524003659593277;
    } else {
        if ((input[1]) <= (3.0500000000000003)) {
            if ((input[2]) <= (4.250000000000001)) {
                var2 = -0.07030875834199876;
            } else {
                if ((input[0]) <= (6.3500000000000005)) {
                    var2 = -0.06982477296636533;
                } else {
                    var2 = -0.06974122225444981;
                }
            }
        } else {
            var2 = -0.05935134690978199;
        }
    }
    double var3;
    if ((input[2]) <= (1.8)) {
        var3 = 0.10422142115935154;
    } else {
        if ((input[2]) <= (4.250000000000001)) {
            var3 = -0.056581139232602384;
        } else {
            if ((input[2]) <= (4.8500000000000005)) {
                var3 = -0.06811407503424083;
            } else {
                if ((input[1]) <= (2.9500000000000006)) {
                    var3 = -0.0675257459921944;
                } else {
                    var3 = -0.06782161711223954;
                }
            }
        }
    }
    double var4;
    if ((input[2]) <= (3.4000000000000004)) {
        if ((input[1]) <= (3.4500000000000006)) {
            var4 = 0.0863032056954337;
        } else {
            var4 = 0.09914564739109;
        }
    } else {
        if ((input[2]) <= (4.8500000000000005)) {
            if ((input[0]) <= (5.8500000000000005)) {
                var4 = -0.06648119153970176;
            } else {
                var4 = -0.06631816120986324;
            }
        } else {
            if ((input[1]) <= (2.9500000000000006)) {
                var4 = -0.06574834101797528;
            } else {
                var4 = -0.06592611534069574;
            }
        }
    }
    double var5;
    if ((input[2]) <= (3.4000000000000004)) {
        if ((input[0]) <= (5.050000000000001)) {
            var5 = 0.07974752538862645;
        } else {
            var5 = 0.09236530150900425;
        }
    } else {
        if ((input[2]) <= (4.8500000000000005)) {
            if ((input[0]) <= (5.8500000000000005)) {
                var5 = -0.06486284477521095;
            } else {
                var5 = -0.06460778135754495;
            }
        } else {
            if ((input[2]) <= (5.550000000000001)) {
                var5 = -0.06429938341616635;
            } else {
                var5 = -0.06414461042315033;
            }
        }
    }
    double var6;
    if ((input[2]) <= (3.4000000000000004)) {
        if ((input[1]) <= (3.4500000000000006)) {
            var6 = 0.07453099257686188;
        } else {
            var6 = 0.08660753989550297;
        }
    } else {
        if ((input[2]) <= (4.8500000000000005)) {
            if ((input[0]) <= (5.8500000000000005)) {
                var6 = -0.0633865062617181;
            } else {
                var6 = -0.06319899799076131;
            }
        } else {
            if ((input[3]) <= (1.9500000000000002)) {
                var6 = -0.06294361522523977;
            } else {
                var6 = -0.06266873448307818;
            }
        }
    }
    double var7;
    if ((input[2]) <= (3.4000000000000004)) {
        if ((input[0]) <= (5.050000000000001)) {
            var7 = 0.0699304933116121;
        } else {
            var7 = 0.0821729945134087;
        }
    } else {
        if ((input[2]) <= (4.8500000000000005)) {
            if ((input[1]) <= (2.85)) {
                var7 = -0.061994856349574926;
            } else {
                var7 = -0.06219275987591127;
            }
        } else {
            if ((input[2]) <= (5.550000000000001)) {
                var7 = -0.06158838592474202;
            } else {
                var7 = -0.06133875650514577;
            }
        }
    }
    double var8;
    if ((input[2]) <= (1.8)) {
        if ((input[0]) <= (5.050000000000001)) {
            var8 = 0.07613926221744755;
        } else {
            var8 = 0.07516599922254297;
        }
    } else {
        if ((input[1]) <= (3.0500000000000003)) {
            if ((input[0]) <= (5.750000000000001)) {
                var8 = -0.06189662412108903;
            } else {
                if ((input[2]) <= (5.050000000000001)) {
                    var8 = -0.060672592266487094;
                } else {
                    var8 = -0.060269919249518224;
                }
            }
        } else {
            var8 = -0.047131506364597904;
        }
    }
    double var9;
    if ((input[2]) <= (3.4000000000000004)) {
        if ((input[1]) <= (3.4500000000000006)) {
            var9 = 0.06327854070156062;
        } else {
            var9 = 0.07539563226571339;
        }
    } else {
        if ((input[2]) <= (5.550000000000001)) {
            if ((input[3]) <= (1.6500000000000001)) {
                if ((input[0]) <= (5.8500000000000005)) {
                    var9 = -0.05975706874719155;
                } else {
                    var9 = -0.0595816630896939;
                }
            } else {
                var9 = -0.06018893023036827;
            }
        } else {
            var9 = -0.05912388706366274;
        }
    }
    double var10;
    var10 = exp(((((((((((0) + (var0)) + (var1)) + (var2)) + (var3)) + (var4)) + (var5)) + (var6)) + (var7)) + (var8)) + (var9));
    double var11;
    if ((input[2]) <= (1.8)) {
        var11 = -1.1952609652674462;
    } else {
        if ((input[2]) <= (4.8500000000000005)) {
            if ((input[1]) <= (2.85)) {
                var11 = -0.9775710567000557;
            } else {
                var11 = -0.9893508136571655;
            }
        } else {
            if ((input[3]) <= (1.9500000000000002)) {
                var11 = -1.1611232296057417;
            } else {
                var11 = -1.1952609652674462;
            }
        }
    }
    double var12;
    if ((input[2]) <= (1.8)) {
        var12 = -0.07151978915296087;
    } else {
        if ((input[2]) <= (4.8500000000000005)) {
            if ((input[0]) <= (5.750000000000001)) {
                var12 = 0.11448389668171499;
            } else {
                var12 = 0.12473617368155408;
            }
        } else {
            if ((input[3]) <= (1.9500000000000002)) {
                var12 = -0.03771482575699713;
            } else {
                var12 = -0.07149803555176153;
            }
        }
    }
    double var13;
    if ((input[2]) <= (1.8)) {
        if ((input[0]) <= (5.050000000000001)) {
            var13 = -0.0691755265051437;
        } else {
            var13 = -0.06917552650514373;
        }
    } else {
        if ((input[3]) <= (1.6500000000000001)) {
            if ((input[2]) <= (4.450000000000001)) {
                var13 = 0.11156568233614622;
            } else {
                var13 = 0.09187625749097966;
            }
        } else {
            if ((input[2]) <= (5.550000000000001)) {
                var13 = -0.05022824742218183;
            } else {
                var13 = -0.0694861084781225;
            }
        }
    }
    double var14;
    if ((input[3]) <= (0.45000000000000007)) {
        if ((input[0]) <= (5.050000000000001)) {
            var14 = -0.06710407335320094;
        } else {
            var14 = -0.06872933368793765;
        }
    } else {
        if ((input[3]) <= (1.6500000000000001)) {
            if ((input[2]) <= (4.450000000000001)) {
                var14 = 0.09790627133627622;
            } else {
                var14 = 0.08361056069221848;
            }
        } else {
            if ((input[2]) <= (5.550000000000001)) {
                var14 = -0.048234513796826806;
            } else {
                var14 = -0.06740930293654418;
            }
        }
    }
    double var15;
    if ((input[2]) <= (1.8)) {
        if ((input[2]) <= (1.4500000000000002)) {
            var15 = -0.06526465569193407;
        } else {
            var15 = -0.06551483179268315;
        }
    } else {
        if ((input[2]) <= (4.8500000000000005)) {
            if ((input[0]) <= (5.750000000000001)) {
                var15 = 0.08325334796008672;
            } else {
                var15 = 0.09454068200248396;
            }
        } else {
            if ((input[2]) <= (5.550000000000001)) {
                var15 = -0.03397826429664227;
            } else {
                var15 = -0.0665430251242125;
            }
        }
    }
    double var16;
    if ((input[3]) <= (0.45000000000000007)) {
        if ((input[0]) <= (5.050000000000001)) {
            var16 = -0.06371784996510085;
        } else {
            var16 = -0.06587329898446664;
        }
    } else {
        if ((input[3]) <= (1.6500000000000001)) {
            if ((input[2]) <= (4.450000000000001)) {
                var16 = 0.0837788467929869;
            } else {
                var16 = 0.07167788334433021;
            }
        } else {
            if ((input[2]) <= (5.550000000000001)) {
                var16 = -0.04524370279073088;
            } else {
                var16 = -0.06390750075509775;
            }
        }
    }
    double var17;
    if ((input[2]) <= (1.8)) {
        if ((input[2]) <= (1.4500000000000002)) {
            var17 = -0.06228316596059768;
        } else {
            var17 = -0.06268285972502645;
        }
    } else {
        if ((input[3]) <= (1.6500000000000001)) {
            if ((input[2]) <= (4.450000000000001)) {
                var17 = 0.08012558894304615;
            } else {
                var17 = 0.06562500280156235;
            }
        } else {
            if ((input[2]) <= (5.550000000000001)) {
                var17 = -0.04269731510939549;
            } else {
                var17 = -0.06249275115465398;
            }
        }
    }
    double var18;
    if ((input[3]) <= (0.45000000000000007)) {
        if ((input[0]) <= (5.050000000000001)) {
            var18 = -0.0611255612881346;
        } else {
            var18 = -0.06349548882129996;
        }
    } else {
        if ((input[2]) <= (4.8500000000000005)) {
            if ((input[0]) <= (5.750000000000001)) {
                var18 = 0.065968817494556;
            } else {
                var18 = 0.0780962002872872;
            }
        } else {
            if ((input[2]) <= (5.550000000000001)) {
                var18 = -0.028799059908564822;
            } else {
                var18 = -0.0628837663348234;
            }
        }
    }
    double var19;
    if ((input[3]) <= (0.45000000000000007)) {
        if ((input[1]) <= (3.4500000000000006)) {
            var19 = -0.060034152193798644;
        } else {
            var19 = -0.06226210499621631;
        }
    } else {
        if ((input[3]) <= (1.6500000000000001)) {
            if ((input[2]) <= (4.450000000000001)) {
                var19 = 0.07031741238533011;
            } else {
                var19 = 0.0591935540961459;
            }
        } else {
            if ((input[2]) <= (5.550000000000001)) {
                var19 = -0.04099054620404253;
            } else {
                var19 = -0.05996545515180032;
            }
        }
    }
    double var20;
    if ((input[3]) <= (0.45000000000000007)) {
        if ((input[1]) <= (3.4500000000000006)) {
            var20 = -0.05899653954605621;
        } else {
            var20 = -0.061480284273085134;
        }
    } else {
        if ((input[3]) <= (1.6500000000000001)) {
            if ((input[2]) <= (4.450000000000001)) {
                var20 = 0.0666920317367002;
            } else {
                var20 = 0.05567446078590549;
            }
        } else {
            if ((input[2]) <= (5.550000000000001)) {
                var20 = -0.039282830952042706;
            } else {
                var20 = -0.05890846656578417;
            }
        }
    }
    double var21;
    var21 = exp(((((((((((0) + (var11)) + (var12)) + (var13)) + (var14)) + (var15)) + (var16)) + (var17)) + (var18)) + (var19)) + (var20));
    double var22;
    if ((input[2]) <= (4.8500000000000005)) {
        if ((input[2]) <= (4.250000000000001)) {
            if ((input[3]) <= (0.45000000000000007)) {
                var22 = -1.1524760761934856;
            } else {
                var22 = -1.1524760761934856;
            }
        } else {
            var22 = -1.1322413652523249;
        }
    } else {
        if ((input[3]) <= (1.9500000000000002)) {
            var22 = -0.9632815288936335;
        } else {
            var22 = -0.9298942558407184;
        }
    }
    double var23;
    if ((input[2]) <= (4.8500000000000005)) {
        if ((input[2]) <= (4.250000000000001)) {
            if ((input[2]) <= (1.8)) {
                var23 = -0.07289116948296916;
            } else {
                var23 = -0.07297314061701872;
            }
        } else {
            var23 = -0.052751607453852795;
        }
    } else {
        if ((input[2]) <= (5.550000000000001)) {
            var23 = 0.10108927541864253;
        } else {
            var23 = 0.12864496049703408;
        }
    }
    double var24;
    if ((input[2]) <= (4.8500000000000005)) {
        if ((input[2]) <= (4.250000000000001)) {
            if ((input[2]) <= (1.8)) {
                var24 = -0.07031576705785895;
            } else {
                var24 = -0.07061494442173064;
            }
        } else {
            var24 = -0.04990895806145997;
        }
    } else {
        if ((input[3]) <= (1.9500000000000002)) {
            var24 = 0.0883497183375826;
        } else {
            var24 = 0.11419390915857204;
        }
    }
    double var25;
    if ((input[3]) <= (1.6500000000000001)) {
        if ((input[2]) <= (4.450000000000001)) {
            if ((input[2]) <= (1.8)) {
                var25 = -0.06806086626311743;
            } else {
                var25 = -0.06861287422151705;
            }
        } else {
            var25 = -0.03188719090355653;
        }
    } else {
        if ((input[0]) <= (6.550000000000001)) {
            var25 = 0.10443236528897847;
        } else {
            var25 = 0.09512862005701817;
        }
    }
    double var26;
    if ((input[2]) <= (4.8500000000000005)) {
        if ((input[2]) <= (4.250000000000001)) {
            if ((input[2]) <= (1.8)) {
                if ((input[2]) <= (1.4500000000000002)) {
                    var26 = -0.0660833938452882;
                } else {
                    var26 = -0.06601404810160398;
                }
            } else {
                var26 = -0.06655218002718898;
            }
        } else {
            var26 = -0.04682024732436426;
        }
    } else {
        if ((input[2]) <= (5.550000000000001)) {
            var26 = 0.07510302825730762;
        } else {
            var26 = 0.0975512889480458;
        }
    }
    double var27;
    if ((input[3]) <= (1.6500000000000001)) {
        if ((input[2]) <= (4.450000000000001)) {
            if ((input[2]) <= (3.4000000000000004)) {
                if ((input[1]) <= (3.4500000000000006)) {
                    var27 = -0.06439070400813855;
                } else {
                    var27 = -0.0643462174858128;
                }
            } else {
                var27 = -0.06504596727226;
            }
        } else {
            var27 = -0.029627856710583877;
        }
    } else {
        if ((input[0]) <= (6.550000000000001)) {
            var27 = 0.09059440470849012;
        } else {
            var27 = 0.08019255916283378;
        }
    }
    double var28;
    if ((input[2]) <= (4.8500000000000005)) {
        if ((input[2]) <= (4.250000000000001)) {
            if ((input[2]) <= (1.8)) {
                if ((input[1]) <= (3.4500000000000006)) {
                    var28 = -0.06291554019220989;
                } else {
                    var28 = -0.06272336016461968;
                }
            } else {
                var28 = -0.06329428077650433;
            }
        } else {
            var28 = -0.04344024781046682;
        }
    } else {
        if ((input[2]) <= (5.550000000000001)) {
            var28 = 0.06450063873186994;
        } else {
            var28 = 0.08577903643426574;
        }
    }
    double var29;
    if ((input[2]) <= (4.8500000000000005)) {
        if ((input[2]) <= (4.250000000000001)) {
            if ((input[2]) <= (1.8)) {
                if ((input[1]) <= (3.4500000000000006)) {
                    var29 = -0.061631619522056404;
                } else {
                    var29 = -0.06134826234181401;
                }
            } else {
                var29 = -0.06188958075829068;
            }
        } else {
            var29 = -0.041718974169119225;
        }
    } else {
        if ((input[2]) <= (5.550000000000001)) {
            var29 = 0.06028504443618404;
        } else {
            var29 = 0.08128266539225362;
        }
    }
    double var30;
    if ((input[2]) <= (4.750000000000001)) {
        if ((input[1]) <= (2.85)) {
            var30 = -0.04786191581498567;
        } else {
            if ((input[3]) <= (0.45000000000000007)) {
                if ((input[1]) <= (3.4500000000000006)) {
                    var30 = -0.0605035848467636;
                } else {
                    var30 = -0.06028420394994585;
                }
            } else {
                var30 = -0.06251547732887337;
            }
        }
    } else {
        if ((input[2]) <= (5.400000000000001)) {
            var30 = 0.04713310115750863;
        } else {
            var30 = 0.07757949238373085;
        }
    }
    double var31;
    if ((input[3]) <= (1.6500000000000001)) {
        if ((input[2]) <= (4.450000000000001)) {
            if ((input[2]) <= (1.8)) {
                if ((input[1]) <= (3.4500000000000006)) {
                    var31 = -0.05936350449845038;
                } else {
                    var31 = -0.05907571145083347;
                }
            } else {
                var31 = -0.060029351394214475;
            }
        } else {
            var31 = -0.02549208865475118;
        }
    } else {
        if ((input[0]) <= (6.550000000000001)) {
            var31 = 0.07481393927460665;
        } else {
            var31 = 0.06207928842731441;
        }
    }
    double var32;
    var32 = exp(((((((((((0) + (var22)) + (var23)) + (var24)) + (var25)) + (var26)) + (var27)) + (var28)) + (var29)) + (var30)) + (var31));
    double var33;
    var33 = ((var10) + (var21)) + (var32);
    assign_array((double[]){(var10) / (var33), (var21) / (var33), (var32) / (var33)}, output, 3);
}
