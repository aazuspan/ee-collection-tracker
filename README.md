## Earth Engine collection tracker

[![Update](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml) [![Deploy](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml) [![Test](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml)

This repository tracks the the availability of selected Earth Engine collections with daily updates at 23:30 UTC. Explore the latest acquisition on the [interactive map](https://aazuspan.github.io/ee-collection-tracker/).

## Collection summary

The table below shows the most recent acquisition `system:time_start` for each tracked collection, along with the time that assets were last queried and updated, and the age of the newest asset during the last query. All times are in UTC.

| Collection ID                             | Last acquisition    | Last update         | Newest asset |
| ----------------------------------------- | ------------------- | ------------------- | ------------ |
| **LANDSAT/LC08/C02/T1**                   | 2026-10-19 15:05:59 | 2026-10-23 23:36:33 | 4 days       |
| **LANDSAT/LC08/C02/T1_TOA**[^derived]     | 2026-10-19 15:05:59 | 2026-10-23 23:36:33 | 4 days       |
| **LANDSAT/LC08/C02/T1_L2**                | 2026-10-17 03:39:47 | 2026-10-23 23:36:33 | 6 days       |
| **LANDSAT/LC09/C02/T1**                   | 2026-10-20 21:36:14 | 2026-10-23 23:36:33 | 3 days       |
| **LANDSAT/LC09/C02/T1_TOA**[^derived]     | 2026-10-20 21:36:14 | 2026-10-23 23:36:33 | 3 days       |
| **LANDSAT/LC09/C02/T1_L2**                | 2026-10-17 17:27:39 | 2026-10-23 23:36:33 | 6 days       |
| **COPERNICUS/S2**                         | 2026-10-23 21:39:34 | 2026-10-23 23:41:04 | 2 hours      |
| **COPERNICUS/S2_HARMONIZED**[^derived]    | 2026-10-23 21:39:34 | 2026-10-23 23:41:04 | 2 hours      |
| **COPERNICUS/S2_SR**                      | 2026-10-23 20:37:44 | 2026-10-23 23:41:04 | 3 hours      |
| **COPERNICUS/S2_SR_HARMONIZED**[^derived] | 2026-10-23 20:37:44 | 2026-10-23 23:41:04 | 3 hours      |
| **NASA/HLS/HLSS30/v002_RAW2**             | 2026-10-21 20:55:09 | 2026-10-23 23:44:13 | 2 days       |
| **NASA/HLS/HLSS30/v002**[^derived]        | 2026-10-21 20:55:09 | 2026-10-23 23:44:13 | 2 days       |
| **NASA/HLS/HLSL30/v002_RAW2**             | 2026-10-20 20:23:59 | 2026-10-23 23:44:13 | 3 days       |
| **NASA/HLS/HLSL30/v002**[^derived]        | 2026-10-20 20:23:59 | 2026-10-23 23:44:13 | 3 days       |

[^derived]: Earth Engine derives this collection by processing another collection on-the-fly. For efficiency, only the source collection is tracked.