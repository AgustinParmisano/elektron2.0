#!/bin/bash
if [ $# -ne 2 ]; then
	echo "Debe pasar 2 parametros: 1: palabra a reemplazar, 2: reemplazo."
	exit 1
fi
echo "Reemplazando todas las ocrrencias de $1 por $2"
$(find ./ -type f -exec sed -i -e "s/$1/$2/g" {} \;)
exit 0
