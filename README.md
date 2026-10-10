## Earth Engine collection tracker

[![Update](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml) [![Deploy](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml) [![Test](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml)

This repository tracks the the availability of selected Earth Engine collections with daily updates at 23:30 UTC. Explore the latest acquisition on the [interactive map](https://aazuspan.github.io/ee-collection-tracker/).

## Collection summary

The table below shows the most recent acquisition `system:time_start` for each tracked collection, along with the time that assets were last queried and updated, and the age of the newest asset during the last query. All times are in UTC.

| Collection ID                             | Last acquisition    | Last update         | Newest asset |
| ----------------------------------------- | ------------------- | ------------------- | ------------ |
| **LANDSAT/LC08/C02/T1**                   | 2026-10-05 14:54:02 | 2026-10-10 23:38:41 | 5 days       |
| **LANDSAT/LC08/C02/T1_TOA**[^derived]     | 2026-10-05 14:54:02 | 2026-10-10 23:38:41 | 5 days       |
| **LANDSAT/LC08/C02/T1_L2**                | 2026-10-05 11:26:18 | 2026-10-10 23:38:41 | 5 days       |
| **LANDSAT/LC09/C02/T1**                   | 2026-10-10 02:48:39 | 2026-10-10 23:38:41 | 21 hours     |
| **LANDSAT/LC09/C02/T1_TOA**[^derived]     | 2026-10-10 02:48:39 | 2026-10-10 23:38:41 | 21 hours     |
| **LANDSAT/LC09/C02/T1_L2**                | 2026-10-08 22:51:37 | 2026-10-10 23:38:41 | 2 days       |
| **COPERNICUS/S2**                         | 2026-10-10 20:39:06 | 2026-10-10 23:41:41 | 3 hours      |
| **COPERNICUS/S2_HARMONIZED**[^derived]    | 2026-10-10 20:39:06 | 2026-10-10 23:41:41 | 3 hours      |
| **COPERNICUS/S2_SR**                      | 2026-10-10 19:44:08 | 2026-10-10 23:41:41 | 4 hours      |
| **COPERNICUS/S2_SR_HARMONIZED**[^derived] | 2026-10-10 19:44:08 | 2026-10-10 23:41:41 | 4 hours      |
| **NASA/HLS/HLSS30/v002_RAW2**             | 2026-10-08 23:38:21 | 2026-10-10 23:44:49 | 2 days       |
| **NASA/HLS/HLSS30/v002**[^derived]        | 2026-10-08 23:38:21 | 2026-10-10 23:44:49 | 2 days       |
| **NASA/HLS/HLSL30/v002_RAW2**             | 2026-10-08 23:46:09 | 2026-10-10 23:44:49 | a day        |
| **NASA/HLS/HLSL30/v002**[^derived]        | 2026-10-08 23:46:09 | 2026-10-10 23:44:49 | a day        |

[^derived]: Earth Engine derives this collection by processing another collection on-the-fly. For efficiency, only the source collection is tracked.