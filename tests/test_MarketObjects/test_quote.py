"""
This file is part of MarketPy. 

MarketPy is a python software package created to help quickly create, (re)build, or 
analyze markets, market structures, and market participants. 

MIT License

Copyright (c) 2016-2017 Peter F. Nabicht

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from cdecimal import Decimal
from nose.tools import *
from MarketPy.MarketObjects.Quote import Quote
from MarketPy.MarketObjects.Price import Price
from MarketPy.MarketObjects.Side import BID_SIDE, ASK_SIDE
from MarketPy.MarketObjects.Product import Product

PROD = Product("MSFT", "Microsoft", Decimal("0.01"), Decimal("0.01"))

def test_quote_creation():
   q = Quote(PROD, BID_SIDE, Price("95.42"), 94)
   assert q.price().price() == Decimal("95.42")
   assert q.visible_qty() == 94
   assert q.hidden_qty() == 0
   assert q._price_level.number_of_orders() == 1
   assert q.product().name() == "Microsoft"
   assert q.product().symbol() == "MSFT"

@raises(AssertionError)
def test_price_does_not_work_for_product():
   #price has to pass the test of being divisible evenly by the product's minimum price increment
   Quote(PROD, BID_SIDE, Price("94.342"), 94)

@raises(AssertionError)
def test_visible_qty_not_negative():
   Quote(PROD, BID_SIDE, Price("94.34"), -3)

@raises(AssertionError)
def test_visible_qty_not_zero():
   Quote(PROD, BID_SIDE, Price("94.34"), 0)

@raises(AssertionError)
def test_hidden_qty_not_negative():
   Quote(PROD, BID_SIDE, Price("94.34"), 23, -23)

def test_equality():
   q1 = Quote(PROD, BID_SIDE, Price("95.42"), 94)
   q2 = Quote(PROD, BID_SIDE, Price("95.42"), 94)
   assert q1 == q2

   q2 = Quote(Product("APPL", "Apple", "0.01", "0.01"), BID_SIDE, Price("95.42"), 94)
   assert q1 != q2

   q2 = Quote(PROD, BID_SIDE, Price("95.43"), 94)
   assert q1 != q2

   q2 = Quote(PROD, BID_SIDE, Price("95.42"), 91)
   assert q1 != q2

   q2 = Quote(PROD, BID_SIDE, Price("95.42"), 94, 2)
   assert q1 != q2

   q2 = Quote(PROD, BID_SIDE, Price("95.42"), 94, 0)
   assert q1 == q2

   q1 = Quote(PROD, BID_SIDE, Price("95.42"), 94, 3)
   q2 = Quote(PROD, BID_SIDE, Price("95.42"), 94, 3)
   assert q1 == q2