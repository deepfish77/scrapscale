from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class Value(BaseModel):
    id: str
    displayValue: str
    value: str
    selected: bool
    selectable: bool
    orderable: bool
    bisnEnabled: bool
    pid: str
    seasonDisplay: Optional[str] = None
    url: str
    inStock: Optional[bool] = None




class Product(BaseModel):
    uuid: str
    id: str
    productName: str
    masterID: str
    productType: str
    pdpSwatches: Dict[str, Any]
    fit: str
    altProductIDs: Any
    sizeChartId: str
    sizeChartModalURL: str
    bisnEnabled: bool
    showAltImagesAtColor: bool
    colorTag: Dict[str, Any]

