# -*- coding: utf-8 -*-


import sys
sys.path.append(u'../ftplugin')

import unittest
from datetime import date
from datetime import timedelta

from orgmode.liborgmode.headings import Heading
from orgmode.liborgmode.orgdate import OrgDate
from orgmode.liborgmode.agendafilter import contains_active_todo
from orgmode.liborgmode.agendafilter import contains_active_date
from orgmode.liborgmode.agendafilter import is_within_week
from orgmode.liborgmode.agendafilter import filter_items


class AgendaTestCase(unittest.TestCase):
	u"""Tests all the functionality of the TODO module."""

	def setUp(self):
		self.text = [ i.encode(u'utf-8') for i in u"""
* TODO Heading 1
  some text
""".split(u'\n') ]


	def test_contains_active_todo(self):
		heading = Heading(title=u'Refactor the code', todo='TODO')
		self.assertTrue(contains_active_todo(heading))

		heading = Heading(title=u'Refactor the code', todo='DONE')
		self.assertFalse(contains_active_todo(heading))

		heading = Heading(title=u'Refactor the code', todo=None)
		self.assertFalse(contains_active_todo(heading))

	def test_contains_active_date(self):
		heading = Heading(title=u'Refactor the code', active_date=None)
		self.assertFalse(contains_active_date(heading))

		odate = OrgDate(True, 2011, 11, 1)
		heading = Heading(title=u'Refactor the code', active_date=odate)
		self.assertTrue(contains_active_date(heading))

	def test_is_within_week(self):
		# to far in the future
		tmpdate = date.today() + timedelta(days=8)
		odate = OrgDate(True, tmpdate.year, tmpdate.month, tmpdate.day)
		heading = Heading(title=u'Refactor the code', active_date=odate)
		self.assertFalse(is_within_week(heading))

		# within a week
		tmpdate = date.today() + timedelta(days=5)
		odate = OrgDate(True, tmpdate.year, tmpdate.month, tmpdate.day)
		heading = Heading(title=u'Refactor the code', active_date=odate)
		self.assertTrue(is_within_week(heading))

		# in the past
		tmpdate = date.today() - timedelta(days=105)
		odate = OrgDate(True, tmpdate.year, tmpdate.month, tmpdate.day)
		heading = Heading(title=u'Refactor the code', active_date=odate)
		self.assertTrue(is_within_week(heading))

	def test_filter_items(self):
		# only headings with date and todo should be returned
		tmpdate = date.today()
		odate = OrgDate(True, tmpdate.year, tmpdate.month, tmpdate.day)
		tmp_head = Heading(title=u'Refactor the code', todo='TODO', active_date=odate)
		headings = [tmp_head]
		filtered = filter_items(headings,
				[contains_active_date, contains_active_todo])

		self.assertEqual(len(filtered), 1)
		self.assertEqual(filtered, headings)

		# try a longer list
		headings = headings * 3
		filtered = filter_items(headings,
				[contains_active_date, contains_active_todo])

		self.assertEqual(len(filtered), 3)
		self.assertEqual(filtered, headings)

		# date does not contain all needed fields thus gets ignored
		tmpdate = date.today()
		odate = OrgDate(True, tmpdate.year, tmpdate.month, tmpdate.day)
		tmp_head = Heading(title=u'Refactor the code', active_date=odate)
		headings = [tmp_head]
		filtered = filter_items(headings, [contains_active_date,
				contains_active_todo])
		self.assertEqual([], filtered)


# vim: set noexpandtab:
