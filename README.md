## Earth Engine collection tracker

[![Update](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml) [![Deploy](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml) [![Test](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml)

This repository tracks the the availability of selected Earth Engine collections with daily updates at 23:30 UTC. Explore the latest acquisition on the [interactive map](https://aazuspan.github.io/ee-collection-tracker/).

## Collection summary

The table below shows the most recent acquisition `system:time_start` for each tracked collection, along with the time that assets were last queried and updated, and the age of the newest asset during the last query. All times are in UTC.

| Collection ID                             | Last acquisition    | Last update         | Newest asset |
| ----------------------------------------- | ------------------- | ------------------- | ------------ |
| **LANDSAT/LC08/C02/T1**                   | 2026-10-13 00:57:55 | 2026-10-14 23:35:46 | a day        |
| **LANDSAT/LC08/C02/T1_TOA**[^derived]     | 2026-10-13 00:57:55 | 2026-10-14 23:35:46 | a day        |
| **LANDSAT/LC08/C02/T1_L2**                | 2026-10-05 13:19:56 | 2026-10-14 23:35:46 | 9 days       |
| **LANDSAT/LC09/C02/T1**                   | 2026-10-14 03:58:26 | 2026-10-14 23:35:46 | 20 hours     |
| **LANDSAT/LC09/C02/T1_TOA**[^derived]     | 2026-10-14 03:58:26 | 2026-10-14 23:35:46 | 20 hours     |
| **LANDSAT/LC09/C02/T1_L2**                | 2026-10-11 23:19:19 | 2026-10-14 23:35:46 | 3 days       |
| **COPERNICUS/S2**                         | 2026-10-14 20:40:02 | 2026-10-14 23:40:19 | 3 hours      |
| **COPERNICUS/S2_HARMONIZED**[^derived]    | 2026-10-14 20:40:02 | 2026-10-14 23:40:19 | 3 hours      |
| **COPERNICUS/S2_SR**                      | 2026-10-14 20:17:57 | 2026-10-14 23:40:19 | 3 hours      |
| **COPERNICUS/S2_SR_HARMONIZED**[^derived] | 2026-10-14 20:17:57 | 2026-10-14 23:40:19 | 3 hours      |
| **NASA/HLS/HLSS30/v002_RAW2**             | 2026-10-11 23:52:31 | 2026-10-14 23:44:19 | 2 days       |
| **NASA/HLS/HLSS30/v002**[^derived]        | 2026-10-11 23:52:31 | 2026-10-14 23:44:19 | 2 days       |
| **NASA/HLS/HLSL30/v002_RAW2**             | 2026-10-11 23:48:45 | 2026-10-14 23:44:19 | 2 days       |
| **NASA/HLS/HLSL30/v002**[^derived]        | 2026-10-11 23:48:45 | 2026-10-14 23:44:19 | 2 days       |

[^derived]: Earth Engine derives this collection by processing another collection on-the-fly. For efficiency, only the source collection is tracked.