import pb


def pkg_comp_name_version(i, x):
    if i.name == x.name:
        if i.version == x.version:
            return 0
        elif i.version < x.version:
            return -1
        else:
            return 1
    elif i.name > x.name:
        return 1
    else:
        return -1


def pkg_comp_name(i, x):
    if i.name == x.name:
        return 0
    elif i.name > x.name:
        return 1
    else:
        return -1


def cmp_bisect(list, key, cmp=cmp):
    lo = 0
    hi = len(list) - 1
    mid = 0
    while (lo <= hi):
        mid = lo + (hi - lo) / 2
        i = cmp(list[mid], key)
        if i < 0:
            lo = mid + 1
        elif i > 0:
            hi = mid - 1
        else:
            break
    if cmp(key,list[mid]) <= 0:
        return mid
    else:
        return mid+1


def floor(list, key, cmp=cmp):
    indx = cmp_bisect(list, key, cmp)
    if indx >= len(list):
        return list[-1]
    c = cmp(list[indx], key)
    if c <= 0:
        return list[indx]
    else:
        return list[indx - 1] if indx > 0 else None


def ceiling(list, key, cmp=cmp):
    indx = cmp_bisect(list, key, cmp)
    if indx >= len(list):
        return None
    c = cmp(list[indx], key)
    if c < 0:
        return list[indx + 1] if indx < len(list) - 1 else None
    else:
        return list[indx]


def lower(list, key, cmp=cmp):
    indx = cmp_bisect(list, key, cmp)
    if indx >= len(list):
        return list[-1]
    c = cmp(list[indx], key)
    if c < 0:
        return list[indx]
    else:
        return list[indx - 1] if indx > 0 else None


def higher(list, key, cmp=cmp):
    indx = cmp_bisect(list, key, cmp)
    if indx >= len(list):
        return None
    c = cmp(list[indx], key)
    if c <= 0:
        return list[indx + 1] if indx < len(list) - 1 else None
    else:
        return list[indx]


def equal(list, key, cmp=cmp):
    indx = cmp_bisect(list, key, cmp)
    if indx >= len(list): return None
    return list[indx] if cmp(list[indx], key) == 0 else None


def pkg_range_query(list, pkg_name, op1="", v1="", op2="", v2=""):
    def complete_version(v):
        tokens = v.split(".")
        for i in range(3 - len(tokens)):
            tokens.push("0")
        return ".".join(tokens)

    #empty version means last version

    if op1 == "==" or op1 == "":
        if v1:
            x = equal(list, pb.Package(pkg_name, complete_version(v1)), pkg_comp_name_version)
        else:
            x = lower(list, pb.Package(pkg_name+'x01', ""), pkg_comp_name)
    elif op1 == "<":
        if v1:
            x = lower(list, pb.Package(pkg_name, complete_version(v1)), pkg_comp_name_version)
        else:
            x = lower(list, pb.Package(pkg_name+'x01', ""), pkg_comp_name)
            x = lower(list, x, pkg_comp_name)
    elif op1 == ">":
        if v1:
            x = higher(list, pb.Package(pkg_name, complete_version(v1)), pkg_comp_name_version)
        else:
            x = None
    elif op1 == "<=":
        if v1:
            x = floor(list, pb.Package(pkg_name, complete_version(v1)), pkg_comp_name_version)
        else:
            x = lower(list, pb.Package(pkg_name+'x01', ""), pkg_comp_name)
    elif op1 == ">=":
        if v1:
            x = ceiling(list, pb.Package(pkg_name, complete_version(v1)), pkg_comp_name_version)
        else:
            x = lower(list, pb.Package(pkg_name+'x01', ""), pkg_comp_name)
    else:
        raise Exception("Invalid operator" + op1)

    if x and x.name != pkg_name:
        return None

    if v2:
        if op2 == "==":
            return x if x.version == complete_version(v2) else None
        elif op2 == "<":
            return x if x.version < complete_version(v2) else None
        elif op2 == ">":
            return x if x.version > complete_version(v2) else None
        elif op2 == "<=":
            return x if x.version <= complete_version(v2) else None
        elif op2 == ">=":
            return x if x.version <= complete_version(v2) else None
        else:
            raise Exception("Invalid operator" + op2)
    else:
        return x
