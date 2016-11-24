# el-rejunte

Pasos para crear un branch y trabajar.

Desde consola linux:

1- Para crear un nuevo branch:

    git checkout -b nuevo_branch

2- Para verificar que estamos en ese branch:    

    git branch -a


A partir de aqui podemos editar el contenido del repositorio local y modificar archivos a placer

3- Para ver el estado de los archivos del repositorio local con respecto al repositorio remoto:

    git status

4- Para agregar los archivos que se desean commitear:

    git add nombre_directorio/nombre_archivo

5- Para commitiar los archivos agregados:

    git commit -m 'Comentario descriptivo'

6- Para pushear el commit al repositorio remoto:

    git push origin nuevo_branch
    


 



