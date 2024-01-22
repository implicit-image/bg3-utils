#!/usr/bin/env python3

import sys

def lvl_on_curve(lvl: int, spare_xp: int, curr_curve: dict, ref_curve: dict):
    # sum total xp
    curr_sum_xp = spare_xp
    # calculate real level
    for xp in curr_curve[:lvl]:
        curr_sum_xp += xp
    print(f"current sum xp is {curr_sum_xp}")
    # find corresponding level on reference curve
    ref_lvl = 0
    ref_spare_xp = curr_sum_xp
    for xp in ref_curve:
        if xp <= ref_spare_xp:
            ref_lvl += 1
            ref_spare_xp -= xp
    return (ref_lvl, ref_spare_xp)

def print_curve_selection(curves: list[dict]) -> None:
    index = 1
    for curve in curves:
        print(f"{curve['name']}: {index}")
        index += 1


def main():

    curves = [
        { #
            "name"  : "release",
            "curve" : [0, 300, 600, 1800, 3800, 6500, 8000, 9000, 12000, 14000, 20000, 24000, 30000, 20000, 25000, 30000, 30000, 40000, 40000, 50000]
        },
        {
            "name": "double xp",
            "curve" : [0, 150, 300, 900, 1900, 3250, 4000, 4500, 6000, 7000, 10000, 12000, 15000, 10000, 12500, 15000, 15000, 20000, 20000, 25000]
        }
    ]

    if len(sys.argv) >= 2 and sys.argv[1] == "-i":
        print("Choose currenly used curve:")
        print_curve_selection(curves)
        curr_curve_id = int(input("Curve number: ")) - 1
        print("Choose curve to compare against: ")
        print_curve_selection(curves)
        ref_curve_id = int(input("Curve number: ")) - 1
        curr_level = int(input("Your current character level: "))
        spare_xp = int(input("XP acquired since last lvlup: "))
        curr_curve = curves[curr_curve_id]['curve']
        ref_curve = curves[ref_curve_id]['curve']
        ref_lvl, ref_xp = lvl_on_curve(curr_level, spare_xp, curr_curve, ref_curve)
        print(f"level {curr_level} and {spare_xp} spare XP on {curves[curr_curve_id]['name']} would be level {ref_lvl} and {ref_xp} spare XP on {curves[ref_curve_id]['name']} ")

if __name__ == "__main__":
    main()
