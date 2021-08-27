"""
python 标准库 glob
glob 文件名模式匹配，不用遍历整个目录判断每个文件是否符合匹配模式
"""
import glob

print('1.星号(*)匹配零个或多个字符:')
for name in glob.glob('dir/*'):
    print(name)
print()
'''
dir/file2.txt
dir/file.txt
dir/file1.txt
dir/subdir
dir/fileb.txt
dir/filea.txt
'''

print('列出子目录中的文件，必须在模式中包括子目录名：')
# 用子目录查询文件
print('Named explicitly:')
for name in glob.glob('dir/subdir/*'):
    print('\t', name)

# 用通配符* 代替子目录名
print('Named with wildcard:')
for name in glob.glob('dir/*/*'):
    print('\t', name)
print()
'''
Named explicitly:
	 dir/subdir/subsubdir
	 dir/subdir/subfile.txt
Named with wildcard:
	 dir/subdir/subsubdir
	 dir/subdir/subfile.txt
'''

print("2.单个字符通配符，用问号(?)匹配任何单个的字符：")
for name in glob.glob('dir/file?.txt'):
    print(name)
print()
'''
dir/file2.txt
dir/file1.txt
dir/fileb.txt
dir/filea.txt
'''

print("3.字符范围，当需要匹配一个特定的字符，可以使用一个范围")
for name in glob.glob('dir/*[0-9].*'):
    print(name)

'''
dir/file1.txt
dir/file2.txt
'''
