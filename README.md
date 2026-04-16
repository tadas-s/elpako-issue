# Elpako Issue

## Context

Elpako software package provides local API to sign data using Lithuanian
identity card.

API docs: https://documenter.getpostman.com/view/11918038/UVJihuNs

Note that local API not using cross-origin request headers seems to be
intentional to allow anyone implement their own data signing applications.

> The local API is for operations with certificates stored in SmartCard
> technology. All SmartCard types issued by LT are supported - RC USB
> signing devices, personal identity cards, government card certificates.
