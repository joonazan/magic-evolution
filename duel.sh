java -Xms1G -Xmx2G -noverify  -Dcom.sun.management.jmxremote -cp magarena:magarena/lib/annotations.jar:magarena/lib/jsr305.jar:magarena/release/lib/groovy-all-*.jar:magarena/release/Magarena.jar  \
-Dmagarena.dir=`pwd`/magarena/release \
-Ddebug=false \
-DparseMissing=false \
-DdevMode=false \
-Dgame.log=10.log \
-Djava.awt.headless=true \
magic.DeckStrCal \
--ai1 MCTS --str1 1 --deck1 $1 \
--ai2 MCTS --str2 1 --deck2 $2 \
--games 1
