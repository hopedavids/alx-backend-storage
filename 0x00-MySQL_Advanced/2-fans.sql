-- A SQL script that ranks country origins of bands, ordered by the number of (non-unique) fans
-- Calculate/compute something is always power intensive… better to distribute the load!

SELECT origin, SUM(nb_fans) AS total_fans
FROM metal_bands
GROUP BY origin
ORDER BY total_fans DESC;