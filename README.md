## Earth Engine collection tracker

[![Update](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml) [![Deploy](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml) [![Test](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml)

This repository tracks the the availability of selected Earth Engine collections with daily updates at 23:30 UTC. Explore the latest acquisition on the [interactive map](https://aazuspan.github.io/ee-collection-tracker/).

## Collection summary

The table below shows the most recent acquisition `system:time_start` for each tracked collection, along with the time that assets were last queried and updated, and the age of the newest asset during the last query. All times are in UTC.

| Collection ID                             | Last acquisition    | Last update         | Newest asset |
| ----------------------------------------- | ------------------- | ------------------- | ------------ |
| **LANDSAT/LC08/C02/T1**                   | 2026-10-26 15:15:00 | 2026-10-29 23:35:26 | 3 days       |
| **LANDSAT/LC08/C02/T1_TOA**[^derived]     | 2026-10-26 15:15:00 | 2026-10-29 23:35:26 | 3 days       |
| **LANDSAT/LC08/C02/T1_L2**                | 2026-10-19 13:37:53 | 2026-10-29 23:35:26 | 10 days      |
| **LANDSAT/LC09/C02/T1**                   | 2026-10-29 03:18:17 | 2026-10-29 23:35:26 | 20 hours     |
| **LANDSAT/LC09/C02/T1_TOA**[^derived]     | 2026-10-29 03:18:17 | 2026-10-29 23:35:26 | 20 hours     |
| **LANDSAT/LC09/C02/T1_L2**                | 2026-10-26 22:38:24 | 2026-10-29 23:35:26 | 3 days       |
| **COPERNICUS/S2**                         | 2026-10-29 21:08:48 | 2026-10-29 23:39:18 | 3 hours      |
| **COPERNICUS/S2_HARMONIZED**[^derived]    | 2026-10-29 21:08:48 | 2026-10-29 23:39:18 | 3 hours      |
| **COPERNICUS/S2_SR**                      | 2026-10-29 19:52:44 | 2026-10-29 23:39:18 | 4 hours      |
| **COPERNICUS/S2_SR_HARMONIZED**[^derived] | 2026-10-29 19:52:44 | 2026-10-29 23:39:18 | 4 hours      |
| **NASA/HLS/HLSS30/v002_RAW2**             | 2026-10-26 23:57:41 | 2026-10-29 23:42:14 | 2 days       |
| **NASA/HLS/HLSS30/v002**[^derived]        | 2026-10-26 23:57:41 | 2026-10-29 23:42:14 | 2 days       |
| **NASA/HLS/HLSL30/v002_RAW2**             | 2026-10-26 23:56:33 | 2026-10-29 23:42:14 | 2 days       |
| **NASA/HLS/HLSL30/v002**[^derived]        | 2026-10-26 23:56:33 | 2026-10-29 23:42:14 | 2 days       |

[^derived]: Earth Engine derives this collection by processing another collection on-the-fly. For efficiency, only the source collection is tracked.