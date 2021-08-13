





def discount_multicourses(student, course):
    # discount logic
    return 0

discount_checks_funcs = [
        discount_multicourses,
]




def run_discount_checks(student, course):
    percentages_list = []
    for check in discount_checks_funcs:
        percentages_list.append(check(student, course))

    highest_discount = max(percentages_list)
    return highest_discount