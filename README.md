## Earth Engine collection tracker

[![Update](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml) [![Deploy](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml) [![Test](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml)

This repository tracks the the availability of selected Earth Engine collections with daily updates at 23:30 UTC. Explore the latest acquisition on the [interactive map](https://aazuspan.github.io/ee-collection-tracker/).

## Collection summary

The table below shows the most recent acquisition `system:time_start` for each tracked collection, along with the time that assets were last queried and updated, and the age of the newest asset during the last query. All times are in UTC.

| Collection ID                             | Last acquisition    | Last update         | Newest asset |
| ----------------------------------------- | ------------------- | ------------------- | ------------ |
| **LANDSAT/LC08/C02/T1**                   | 2026-11-17 14:42:26 | 2026-11-20 23:34:39 | 3 days       |
| **LANDSAT/LC08/C02/T1_TOA**[^derived]     | 2026-11-17 14:42:26 | 2026-11-20 23:34:39 | 3 days       |
| **LANDSAT/LC08/C02/T1_L2**                | 2026-11-10 09:28:49 | 2026-11-20 23:34:39 | 10 days      |
| **LANDSAT/LC09/C02/T1**                   | 2026-11-20 01:09:58 | 2026-11-20 23:34:39 | 22 hours     |
| **LANDSAT/LC09/C02/T1_TOA**[^derived]     | 2026-11-20 01:09:58 | 2026-11-20 23:34:39 | 22 hours     |
| **LANDSAT/LC09/C02/T1_L2**                | 2026-11-18 22:45:26 | 2026-11-20 23:34:39 | 2 days       |
| **COPERNICUS/S2**                         | 2026-11-20 21:48:17 | 2026-11-20 23:39:32 | 2 hours      |
| **COPERNICUS/S2_HARMONIZED**[^derived]    | 2026-11-20 21:48:17 | 2026-11-20 23:39:32 | 2 hours      |
| **COPERNICUS/S2_SR**                      | 2026-11-20 21:19:20 | 2026-11-20 23:39:32 | 2 hours      |
| **COPERNICUS/S2_SR_HARMONIZED**[^derived] | 2026-11-20 21:19:20 | 2026-11-20 23:39:32 | 2 hours      |
| **NASA/HLS/HLSS30/v002_RAW2**             | 2026-11-17 22:54:19 | 2026-11-20 23:42:22 | 3 days       |
| **NASA/HLS/HLSS30/v002**[^derived]        | 2026-11-17 22:54:19 | 2026-11-20 23:42:22 | 3 days       |
| **NASA/HLS/HLSL30/v002_RAW2**             | 2026-11-17 23:46:15 | 2026-11-20 23:42:22 | 2 days       |
| **NASA/HLS/HLSL30/v002**[^derived]        | 2026-11-17 23:46:15 | 2026-11-20 23:42:22 | 2 days       |

[^derived]: Earth Engine derives this collection by processing another collection on-the-fly. For efficiency, only the source collection is tracked.