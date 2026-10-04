## Earth Engine collection tracker

[![Update](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml) [![Deploy](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml) [![Test](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml)

This repository tracks the the availability of selected Earth Engine collections with daily updates at 23:30 UTC. Explore the latest acquisition on the [interactive map](https://aazuspan.github.io/ee-collection-tracker/).

## Collection summary

The table below shows the most recent acquisition `system:time_start` for each tracked collection, along with the time that assets were last queried and updated, and the age of the newest asset during the last query. All times are in UTC.

| Collection ID                             | Last acquisition    | Last update         | Newest asset |
| ----------------------------------------- | ------------------- | ------------------- | ------------ |
| **LANDSAT/LC08/C02/T1**                   | 2026-09-27 07:29:01 | 2026-10-04 04:10:17 | 6 days       |
| **LANDSAT/LC08/C02/T1_TOA**[^derived]     | 2026-09-27 07:29:01 | 2026-10-04 04:10:17 | 6 days       |
| **LANDSAT/LC08/C02/T1_L2**                | 2026-09-27 05:39:46 | 2026-10-04 04:10:17 | 6 days       |
| **LANDSAT/LC09/C02/T1**                   | 2026-10-03 06:02:36 | 2026-10-04 04:10:17 | 22 hours     |
| **LANDSAT/LC09/C02/T1_TOA**[^derived]     | 2026-10-03 06:02:36 | 2026-10-04 04:10:17 | 22 hours     |
| **LANDSAT/LC09/C02/T1_L2**                | 2026-10-01 22:39:01 | 2026-10-04 04:10:17 | 2 days       |
| **COPERNICUS/S2**                         | 2026-10-04 01:25:57 | 2026-10-04 04:28:06 | 3 hours      |
| **COPERNICUS/S2_HARMONIZED**[^derived]    | 2026-10-04 01:25:57 | 2026-10-04 04:28:06 | 3 hours      |
| **COPERNICUS/S2_SR**                      | 2026-10-04 01:25:15 | 2026-10-04 04:28:06 | 3 hours      |
| **COPERNICUS/S2_SR_HARMONIZED**[^derived] | 2026-10-04 01:25:15 | 2026-10-04 04:28:06 | 3 hours      |
| **NASA/HLS/HLSS30/v002_RAW2**             | 2026-10-01 23:52:31 | 2026-10-04 04:22:46 | 2 days       |
| **NASA/HLS/HLSS30/v002**[^derived]        | 2026-10-01 23:52:31 | 2026-10-04 04:22:46 | 2 days       |
| **NASA/HLS/HLSL30/v002_RAW2**             | 2026-10-01 23:59:59 | 2026-10-04 04:22:46 | 2 days       |
| **NASA/HLS/HLSL30/v002**[^derived]        | 2026-10-01 23:59:59 | 2026-10-04 04:22:46 | 2 days       |

[^derived]: Earth Engine derives this collection by processing another collection on-the-fly. For efficiency, only the source collection is tracked.