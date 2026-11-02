## Earth Engine collection tracker

[![Update](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/update.yaml) [![Deploy](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/pages.yaml) [![Test](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml/badge.svg)](https://github.com/aazuspan/ee-collection-tracker/actions/workflows/test.yaml)

This repository tracks the the availability of selected Earth Engine collections with daily updates at 23:30 UTC. Explore the latest acquisition on the [interactive map](https://aazuspan.github.io/ee-collection-tracker/).

## Collection summary

The table below shows the most recent acquisition `system:time_start` for each tracked collection, along with the time that assets were last queried and updated, and the age of the newest asset during the last query. All times are in UTC.

| Collection ID                             | Last acquisition    | Last update         | Newest asset |
| ----------------------------------------- | ------------------- | ------------------- | ------------ |
| **LANDSAT/LC08/C02/T1**                   | 2026-10-26 15:15:00 | 2026-11-02 23:34:49 | 7 days       |
| **LANDSAT/LC08/C02/T1_TOA**[^derived]     | 2026-10-26 15:15:00 | 2026-11-02 23:34:49 | 7 days       |
| **LANDSAT/LC08/C02/T1_L2**                | 2026-10-26 13:44:06 | 2026-11-02 23:34:49 | 7 days       |
| **LANDSAT/LC09/C02/T1**                   | 2026-11-02 06:16:10 | 2026-11-02 23:34:49 | 17 hours     |
| **LANDSAT/LC09/C02/T1_TOA**[^derived]     | 2026-11-02 06:16:10 | 2026-11-02 23:34:49 | 17 hours     |
| **LANDSAT/LC09/C02/T1_L2**                | 2026-10-31 22:57:21 | 2026-11-02 23:34:49 | 2 days       |
| **COPERNICUS/S2**                         | 2026-11-02 21:40:24 | 2026-11-02 23:38:48 | 2 hours      |
| **COPERNICUS/S2_HARMONIZED**[^derived]    | 2026-11-02 21:40:24 | 2026-11-02 23:38:48 | 2 hours      |
| **COPERNICUS/S2_SR**                      | 2026-11-02 21:40:24 | 2026-11-02 23:38:48 | 2 hours      |
| **COPERNICUS/S2_SR_HARMONIZED**[^derived] | 2026-11-02 21:40:24 | 2026-11-02 23:38:48 | 2 hours      |
| **NASA/HLS/HLSS30/v002_RAW2**             | 2026-10-31 23:52:31 | 2026-11-02 23:42:07 | a day        |
| **NASA/HLS/HLSS30/v002**[^derived]        | 2026-10-31 23:52:31 | 2026-11-02 23:42:07 | a day        |
| **NASA/HLS/HLSL30/v002_RAW2**             | 2026-10-31 23:52:49 | 2026-11-02 23:42:07 | a day        |
| **NASA/HLS/HLSL30/v002**[^derived]        | 2026-10-31 23:52:49 | 2026-11-02 23:42:07 | a day        |

[^derived]: Earth Engine derives this collection by processing another collection on-the-fly. For efficiency, only the source collection is tracked.