## Earth Engine collection tracker

[![Update](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml) [![Deploy](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml) [![Test](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml)

This repository tracks the the availability of selected Earth Engine collections with daily updates at 23:30 UTC. Explore the latest acquisition on the [interactive map](https://aazuspan.github.io/ee-collection-tracker/).

## Collection summary

The table below shows the most recent acquisition `system:time_start` for each tracked collection, along with the time that assets were last queried and updated, and the age of the newest asset during the last query. All times are in UTC.

| Collection ID                             | Last acquisition    | Last update         | Newest asset |
| ----------------------------------------- | ------------------- | ------------------- | ------------ |
| **LANDSAT/LC08/C02/T1**                   | 2026-10-19 15:05:59 | 2026-10-26 23:37:38 | 7 days       |
| **LANDSAT/LC08/C02/T1_TOA**[^derived]     | 2026-10-19 15:05:59 | 2026-10-26 23:37:38 | 7 days       |
| **LANDSAT/LC08/C02/T1_L2**                | 2026-10-19 13:37:53 | 2026-10-26 23:37:38 | 7 days       |
| **LANDSAT/LC09/C02/T1**                   | 2026-10-26 04:35:52 | 2026-10-26 23:37:38 | 19 hours     |
| **LANDSAT/LC09/C02/T1_TOA**[^derived]     | 2026-10-26 04:35:52 | 2026-10-26 23:37:38 | 19 hours     |
| **LANDSAT/LC09/C02/T1_L2**                | 2026-10-24 22:51:34 | 2026-10-26 23:37:38 | 2 days       |
| **COPERNICUS/S2**                         | 2026-10-26 19:18:58 | 2026-10-26 23:40:31 | 4 hours      |
| **COPERNICUS/S2_HARMONIZED**[^derived]    | 2026-10-26 19:18:58 | 2026-10-26 23:40:31 | 4 hours      |
| **COPERNICUS/S2_SR**                      | 2026-10-26 19:18:58 | 2026-10-26 23:40:31 | 4 hours      |
| **COPERNICUS/S2_SR_HARMONIZED**[^derived] | 2026-10-26 19:18:58 | 2026-10-26 23:40:31 | 4 hours      |
| **NASA/HLS/HLSS30/v002_RAW2**             | 2026-10-24 23:57:41 | 2026-10-26 23:43:32 | a day        |
| **NASA/HLS/HLSS30/v002**[^derived]        | 2026-10-24 23:57:41 | 2026-10-26 23:43:32 | a day        |
| **NASA/HLS/HLSL30/v002_RAW2**             | 2026-10-24 23:44:57 | 2026-10-26 23:43:32 | a day        |
| **NASA/HLS/HLSL30/v002**[^derived]        | 2026-10-24 23:44:57 | 2026-10-26 23:43:32 | a day        |

[^derived]: Earth Engine derives this collection by processing another collection on-the-fly. For efficiency, only the source collection is tracked.