# uso: bash fea_folha.sh video.mp4 prefixo  -> folhas de 40 quadros (1 a cada 3 s, 10x4)
. "${FEA_ENV:-./env.sh}"
$F -nostdin -v error -y -i "$1" -vf "fps=1/3,scale=144:256,tile=10x4" "$2_%02d.png"
