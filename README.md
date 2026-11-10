## Earth Engine collection tracker

[![Update](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml) [![Deploy](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml) [![Test](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml)

This repository tracks the the availability of selected Earth Engine collections with daily updates at 23:30 UTC. Explore the latest acquisition on the [interactive map](https://aazuspan.github.io/ee-collection-tracker/).

## Collection summary

The table below shows the most recent acquisition `system:time_start` for each tracked collection, along with the time that assets were last queried and updated, and the age of the newest asset during the last query. All times are in UTC.

| Collection ID                             | Last acquisition    | Last update         | Newest asset |
| ----------------------------------------- | ------------------- | ------------------- | ------------ |
| **LANDSAT/LC08/C02/T1**                   | 2026-11-03 14:01:44 | 2026-11-10 23:34:19 | 7 days       |
| **LANDSAT/LC08/C02/T1_TOA**[^derived]     | 2026-11-03 14:01:44 | 2026-11-10 23:34:19 | 7 days       |
| **LANDSAT/LC08/C02/T1_L2**                | 2026-10-26 13:44:06 | 2026-11-10 23:34:19 | 15 days      |
| **LANDSAT/LC09/C02/T1**                   | 2026-11-03 13:39:45 | 2026-11-10 23:34:19 | 7 days       |
| **LANDSAT/LC09/C02/T1_TOA**[^derived]     | 2026-11-03 13:39:45 | 2026-11-10 23:34:19 | 7 days       |
| **LANDSAT/LC09/C02/T1_L2**                | 2026-11-02 22:45:24 | 2026-11-10 23:34:19 | 8 days       |
| **COPERNICUS/S2**                         | 2026-11-10 21:40:42 | 2026-11-10 23:39:18 | 2 hours      |
| **COPERNICUS/S2_HARMONIZED**[^derived]    | 2026-11-10 21:40:42 | 2026-11-10 23:39:18 | 2 hours      |
| **COPERNICUS/S2_SR**                      | 2026-11-10 20:58:50 | 2026-11-10 23:39:18 | 3 hours      |
| **COPERNICUS/S2_SR_HARMONIZED**[^derived] | 2026-11-10 20:58:50 | 2026-11-10 23:39:18 | 3 hours      |
| **NASA/HLS/HLSS30/v002_RAW2**             | 2026-11-04 23:57:49 | 2026-11-10 23:43:45 | 5 days       |
| **NASA/HLS/HLSS30/v002**[^derived]        | 2026-11-04 23:57:49 | 2026-11-10 23:43:45 | 5 days       |
| **NASA/HLS/HLSL30/v002_RAW2**             | 2026-11-04 23:50:25 | 2026-11-10 23:43:45 | 5 days       |
| **NASA/HLS/HLSL30/v002**[^derived]        | 2026-11-04 23:50:25 | 2026-11-10 23:43:45 | 5 days       |

[^derived]: Earth Engine derives this collection by processing another collection on-the-fly. For efficiency, only the source collection is tracked.