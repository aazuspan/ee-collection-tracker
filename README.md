## Earth Engine collection tracker

[![Update](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml) [![Deploy](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml) [![Test](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml)

This repository tracks the the availability of selected Earth Engine collections with daily updates at 23:30 UTC. Explore the latest acquisition on the [interactive map](https://aazuspan.github.io/ee-collection-tracker/).

## Collection summary

The table below shows the most recent acquisition `system:time_start` for each tracked collection, along with the time that assets were last queried and updated, and the age of the newest asset during the last query. All times are in UTC.

| Collection ID                             | Last acquisition    | Last update         | Newest asset |
| ----------------------------------------- | ------------------- | ------------------- | ------------ |
| **LANDSAT/LC08/C02/T1**                   | 2026-11-10 11:04:55 | 2026-11-17 23:34:39 | 7 days       |
| **LANDSAT/LC08/C02/T1_TOA**[^derived]     | 2026-11-10 11:04:55 | 2026-11-17 23:34:39 | 7 days       |
| **LANDSAT/LC08/C02/T1_L2**                | 2026-11-08 22:51:51 | 2026-11-17 23:34:39 | 9 days       |
| **LANDSAT/LC09/C02/T1**                   | 2026-11-16 14:32:37 | 2026-11-17 23:34:39 | a day        |
| **LANDSAT/LC09/C02/T1_TOA**[^derived]     | 2026-11-16 14:32:37 | 2026-11-17 23:34:39 | a day        |
| **LANDSAT/LC09/C02/T1_L2**                | 2026-11-15 23:58:37 | 2026-11-17 23:34:39 | a day        |
| **COPERNICUS/S2**                         | 2026-11-16 22:10:48 | 2026-11-17 23:38:23 | a day        |
| **COPERNICUS/S2_HARMONIZED**[^derived]    | 2026-11-16 22:10:48 | 2026-11-17 23:38:23 | a day        |
| **COPERNICUS/S2_SR**                      | 2026-11-16 22:10:48 | 2026-11-17 23:38:23 | a day        |
| **COPERNICUS/S2_SR_HARMONIZED**[^derived] | 2026-11-16 22:10:48 | 2026-11-17 23:38:23 | a day        |
| **NASA/HLS/HLSS30/v002_RAW2**             | 2026-11-05 23:52:29 | 2026-11-17 23:41:38 | 11 days      |
| **NASA/HLS/HLSS30/v002**[^derived]        | 2026-11-05 23:52:29 | 2026-11-17 23:41:38 | 11 days      |
| **NASA/HLS/HLSL30/v002_RAW2**             | 2026-11-05 23:58:13 | 2026-11-17 23:41:38 | 11 days      |
| **NASA/HLS/HLSL30/v002**[^derived]        | 2026-11-05 23:58:13 | 2026-11-17 23:41:38 | 11 days      |

[^derived]: Earth Engine derives this collection by processing another collection on-the-fly. For efficiency, only the source collection is tracked.