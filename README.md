## Earth Engine collection tracker

[![Update](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml) [![Deploy](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml) [![Test](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml)

This repository tracks the the availability of selected Earth Engine collections with daily updates at 23:30 UTC. Explore the latest acquisition on the [interactive map](https://aazuspan.github.io/ee-collection-tracker/).

## Collection summary

The table below shows the most recent acquisition `system:time_start` for each tracked collection, along with the time that assets were last queried and updated, and the age of the newest asset during the last query. All times are in UTC.

| Collection ID                             | Last acquisition    | Last update         | Newest asset |
| ----------------------------------------- | ------------------- | ------------------- | ------------ |
| **LANDSAT/LC08/C02/T1**                   | 2026-10-26 15:15:00 | 2026-10-28 23:35:25 | 2 days       |
| **LANDSAT/LC08/C02/T1_TOA**[^derived]     | 2026-10-26 15:15:00 | 2026-10-28 23:35:25 | 2 days       |
| **LANDSAT/LC08/C02/T1_L2**                | 2026-10-19 13:37:53 | 2026-10-28 23:35:25 | 9 days       |
| **LANDSAT/LC09/C02/T1**                   | 2026-10-27 22:57:45 | 2026-10-28 23:35:25 | a day        |
| **LANDSAT/LC09/C02/T1_TOA**[^derived]     | 2026-10-27 22:57:45 | 2026-10-28 23:35:25 | a day        |
| **LANDSAT/LC09/C02/T1_L2**                | 2026-10-26 22:38:24 | 2026-10-28 23:35:25 | 2 days       |
| **COPERNICUS/S2**                         | 2026-10-28 20:40:18 | 2026-10-28 23:38:44 | 3 hours      |
| **COPERNICUS/S2_HARMONIZED**[^derived]    | 2026-10-28 20:40:18 | 2026-10-28 23:38:44 | 3 hours      |
| **COPERNICUS/S2_SR**                      | 2026-10-28 20:21:35 | 2026-10-28 23:38:44 | 3 hours      |
| **COPERNICUS/S2_SR_HARMONIZED**[^derived] | 2026-10-28 20:21:35 | 2026-10-28 23:38:44 | 3 hours      |
| **NASA/HLS/HLSS30/v002_RAW2**             | 2026-10-26 23:57:41 | 2026-10-28 23:43:12 | a day        |
| **NASA/HLS/HLSS30/v002**[^derived]        | 2026-10-26 23:57:41 | 2026-10-28 23:43:12 | a day        |
| **NASA/HLS/HLSL30/v002_RAW2**             | 2026-10-26 23:56:33 | 2026-10-28 23:43:12 | a day        |
| **NASA/HLS/HLSL30/v002**[^derived]        | 2026-10-26 23:56:33 | 2026-10-28 23:43:12 | a day        |

[^derived]: Earth Engine derives this collection by processing another collection on-the-fly. For efficiency, only the source collection is tracked.