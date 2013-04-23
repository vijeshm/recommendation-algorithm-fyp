u.item contains the list of movies from the 100k dataset
run 'url.py'. It will fetch the details of the movies in u.item, clean some of the hardcoded attributes and place it in movielens_100k
The urls in the movielens 100k dataset are inconsistent.
The "and 1 more credit" and stuff have been manually removed.

Some of the movie IDs that gave a problem:
267, 271, 312, 351, 1358
1420 - Gilligan Island, The Movie - information is missing!

Duplicates:
imdb_id tt0119349 [u'305', u'865']
imdb_id tt0119594 [u'911', u'1592'] Solved
imdb_id tt0120382 [u'1127', u'1547'] Solved
imdb_id tt0109255 [u'1202', u'1504']
imdb_id tt0117773 [u'711', u'1658'] 
imdb_id tt0114345 [u'1442', u'1542'] Solved
imdb_id tt0120402 [u'297', u'303'] 
imdb_id tt0113670 [u'1063', u'1473'] Solved
imdb_id tt0100404 [u'643', u'1125'] Solved
imdb_id tt0056172 [u'511', u'512'] Solved
imdb_id tt0118842 [u'246', u'268']
imdb_id tt0101540 [u'218', u'1520'] Solved
imdb_id tt0119327 [u'1175', u'1617']
imdb_id tt0119695 [u'876', u'881']
imdb_id tt0119527 [u'309', u'1606']
imdb_id tt0120317 [u'878', u'1003']
imdb_id tt0119338 [u'1395', u'1607']
imdb_id tt0368008 [u'503', u'657'] Solved
imdb_id tt0118836 [u'1234', u'1654']
imdb_id tt0118804 [u'1645', u'1650']
imdb_id tt0116329 [u'304', u'500']
imdb_id tt0071562 [u'127', u'187'] Solved
imdb_id tt0118964 [u'1256', u'1257']
imdb_id tt0118966 [u'329', u'348']
imdb_id tt0106452 [u'445', u'573', u'670'] Solved Partially
imdb_id tt0103064 [u'96', u'195'] Solved
imdb_id tt0119791 [u'1477', u'1625']
imdb_id tt0119484 [u'266', u'680']
imdb_id tt0120148 [u'1429', u'1680']
