outdir="$(realpath "${outdir:-.}")"
ver="$(sed -n 's/.*project(TDLib VERSION \([0-9]*\.[0-9]*\.[0-9]*\).*/\1/p' tdlib/CMakeLists.txt)"
cp tdlib.obsinfo "${outdir}/tdlib.obsinfo" ||:
sed -i "s/version:.*/version: ${ver}/g;" "${outdir}/tdlib.obsinfo"
