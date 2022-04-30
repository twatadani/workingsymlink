''' workingsymlink.py - Working Directoryにシンボリックリンクを作成する '''

import asyncio
import json
import os
import os.path
import traceback
import sys

def load_config() -> dict:
    ''' カレントディレクトリからworkingsymlink_config.json
    を読み込み、dictにして返す
    '''
    with open('workingsymlink_config.json', mode='rt') as fp:
        cfdict = json.load(fp)
    return cfdict

async def create_symlink(filename, src_dir, dst_dir, abspath: bool) -> None:
    ''' シンボリックリンクを作成する '''
    fullsrc = os.path.join(src_dir, filename)
    isdir = os.path.isdir(fullsrc)
    fulldst = os.path.join(dst_dir, filename)
    if abspath:
        fullsrc = os.path.abspath(fullsrc)
    else:
        fullsrc = os.path.relpath(fullsrc, start=dst_dir)

    try:
        os.symlink(fullsrc, fulldst, target_is_directory=isdir)
        print(filename, 'のシンボリックリンクを作成しました。')
    except:
        traceback.print_exc()
    return

async def create_target(dstdir: str, srcdir: str, filename: str,
    link_ext: list, excludes: list, abspath: bool) -> None:
    ''' ターゲットのリンクまたはディレクトリを作成する '''
    dstfull = os.path.join(dstdir, filename)
    srcfull = os.path.join(srcdir, filename)
    if os.path.exists(dstfull):
        print(dstfull, 'はすでに存在するため作成しません。')
    elif not os.path.exists(srcfull):
        print(srcfull, 'が存在しないためリンクまたはディレクトリを作成できません。')
    elif os.path.isdir(srcfull):
        print(dstfull, 'ディレクトリを作成します。')
        os.makedirs(dstfull)
        targets = await list_targets(srcfull, link_ext, excludes)
        coros = [ create_target(dstfull, srcfull, x, link_ext, excludes, abspath) for x in targets ]
        await asyncio.gather(*coros)
    else:
        await create_symlink(filename, srcdir, dstdir, abspath)


def ext(filename: str) -> str:
    ''' 拡張子を抽出する '''
    split = os.path.splitext(filename)
    return split[0] if split[0].startswith('.') else split[-1]

async def list_targets(src_dir: str, link_exts: list, excludes: list) -> None:
    ''' シンボリックリンクを作成するターゲットのリストを作成する '''
    assert src_dir is not None
    assert isinstance(src_dir, str)
    assert os.path.isdir(src_dir), src_dir + 'は存在するディレクトリではありません。'

    crude_list = os.listdir(src_dir)
    target_list = [ x for x in crude_list if 
        (os.path.isdir(os.path.join(src_dir, x)) or
        ext(x) in link_exts) and
        not x in excludes
    ]
    return target_list

async def main() -> None:
    ''' workingsymlinkのメインルーチン '''

    ''' コマンドライン引数のチェック '''
    if len(sys.argv) < 1:
        print('Usage:', __file__, ' source_dir')
        return
    srcdir = sys.argv[1]
    srcdir = os.path.expanduser(os.path.expandvars(srcdir))
    srcdir = os.path.abspath(srcdir)

    ''' コンフィグの読み込み '''
    cfdict = load_config()

    abspath = cfdict['ABSPATH']

    targets = await list_targets(srcdir, cfdict['SymLink_EXT'], cfdict['EXCLUDE'])
    coros = [ create_target(os.getcwd(), srcdir, x, cfdict['SymLink_EXT'], cfdict['EXCLUDE'], abspath) for x in targets ]
    await asyncio.gather(*coros)
    return

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        traceback.print_exc()
