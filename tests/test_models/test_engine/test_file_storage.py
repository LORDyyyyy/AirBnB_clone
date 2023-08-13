#!/usr/bin/python3

"""Unit tests for the FileStorage Class."""

from os import remove
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models import storage
import unittest
import json
from os.path import exists


class TestFileStorage(unittest.TestCase):
    """Unit tests for the FileStorage Class."""

    def setUp(self):
        """Set up test environment."""
        self.fs = FileStorage()
        self.bm = BaseModel()
        self.fs.new(self.bm)

    def tearDown(self):
        """Tear down test environment."""
        del self.fs
        del self.bm

    def test_attributes(self):
        """Test the existence of FileStorage Class Attirbutes."""
        self.assertEqual(type(self.fs._FileStorage__file_path), str)
        self.assertEqual(type(self.fs._FileStorage__objects), dict)
        self.assertTrue(hasattr(self.fs, "_FileStorage__file_path"))
        self.assertTrue(hasattr(self.fs, "_FileStorage__objects"))

    def test_all(self):
        """Test all method."""
        self.assertIsInstance(self.fs, FileStorage)
        self.assertIsNotNone(self.fs.all())
        self.assertIsInstance(self.fs.all(), dict)
        self.assertIs(self.fs.all(), storage._FileStorage__objects)

    def test_new(self):
        """Test the 'all' method and creating new objects."""
        cls_name = self.bm.__class__.__name__
        self.assertEqual(self.fs.all()[f"{cls_name}.{self.bm.id}"], self.bm)

    def test_save(self):
        """Test the 'save' method and JSON file creation."""
        self.fs.save()
        self.assertTrue(exists("./file.json"))
        with open("./file.json", "r") as file:
            cls_name = self.bm.__class__.__name__
            self.assertEqual(json.load(file)[f"{cls_name}.{self.bm.id}"],
                             self.bm.to_dict())

    def test_reload(self):
        """Test the 'reload' method."""
        self.fs.save()
        self.fs.reload()
        cls_name = self.bm.__class__.__name__
        self.assertEqual(self.fs.all()[f"{cls_name}.{self.bm.id}"].id,
                         self.bm.id)

    def test_reload_v2(self):
        """Test reload method which is from FileStorage Class."""
        self.bm.name = 'Mohammed'
        self.bm.save()
        storage.reload()
        reloaded_bm = storage.all()[f'{self.bm.__class__.__name__}'
                                    f'.{self.bm.id}']
        self.assertEqual(reloaded_bm.name, 'Mohammed')

    def test_reload_v3(self):
        """Tests method: reload (reloads objects from string file)."""
        try:
            remove("file.json")
        except Exception:
            pass
        with open("file.json", "w") as file:
            file.write("{}")
        with open("file.json", "r") as file:
            self.assertEqual(json.load(file), {})
