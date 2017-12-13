VIDEONAME=ADOS_0
VIDEOID=8
CUR=$PWD
IMAGEPATH=$PWD/data/image/$VIDEONAME/test/$VIDEOID

cd $IMAGEPATH
sed -i "s,/Users/sunsheng/Desktop/test/$VIDEOID,$IMAGEPATH,g" *.xml

cd $CUR
