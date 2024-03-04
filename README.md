# scaling
Scripts permettant le prétraitement de données de précipitation et de température afin de calculer le scaling des précipitations extrêmes ainsi que le post-traitement pour obtenir les figures correspondantes.

1_Preprocessing_old_multiproduits_IDL.pro est un script IDL que j'utilisais au cours de ma thèse pour faire le prétraitement des données et de calculer les statistiques du scaling sur plusieurs produits de température et de précipitation.

1_Preprocessing.py est un script python permettant le prétraitement des données et de calculer les statistiques. Il est sensé être équivalent au script IDL. Je l'ai crée sans pouvoir le tester sur les données girafe mais il donne tous les éléments clés pour s'en sortir.

2_Figures_old_multiproduits.py est un script python permettant le tracer des figures du scaling. C'est le script que j'utilisais durant ma thèse et qui permet le tracer de plusieurs produits de température et précipitation à la fois.

2_Figures.py est un script python permettant le tracer des figures du scaling. Il est la version simplifiée du script 2_Figures_old_multiproduits.py que j'ai crée sur le champs et qui constitue une bonne base de départ pour tracer les figures à partir du prétraitement des données.


