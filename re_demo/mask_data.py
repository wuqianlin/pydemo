import re

# "(-svn_user'\s)('.*?')(,\s'-svn_password',\s)('.*?')(.*)",
# r"\1'脱敏处理'\3'脱敏处理'\5", exception, count = 1)

def svn_exception_mask(exception: str):
    masked_line = re.sub(
        "(\s-svn_user\s)(.*?)(\s-svn_password\s)(.*?)(\s.*)",
        r"\1脱敏处理\3脱敏处理\5", exception, count=1)
    return masked_line


def main():
    ms = "dpiv3 -svn_server 192.168.6.200 -svn_user chenn -svn_password fd223f -svn_url_suffix " \
         "/BRDCDLIB/Modules/byUnifiedDPI/branches/china_unicom/china_unicom_V3_20191115_231952_20200102 -revision " \
         "238175  -libcom /BRDCDLIB/Modules/byLibcom/trunk:234357 -bybase /BRDCDLIB/Modules/byBase/trunk:237464 " \
         "-build_args js_unicom -version 238175 "
    r_m = svn_exception_mask(ms)
    print(r_m)

if __name__ == '__main__':
    main()