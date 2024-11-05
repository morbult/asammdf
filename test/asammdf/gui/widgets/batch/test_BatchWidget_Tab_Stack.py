#!/usr/bin/env python
from pathlib import Path
from unittest import mock

from PySide6 import QtCore, QtTest

from test.asammdf.gui.widgets.test_BaseBatchWidget import TestBatchWidget

# Note: If it's possible and make sense, use self.subTests
# to avoid initializing widgets multiple times and consume time.


class TestPushButtons(TestBatchWidget):
    default_test_file = "ASAP2_Demo_V171.mf4"
    class_test_file = "test_batch.mf4"

    def setUp(self):
        """
        Events
            - Open 'BatchWidget' with 2 valid measurement.
            - Go to Tab: "Stack"
        """
        super().setUp()
        self.copy_mdf_files_to_workspace()

        # Setup
        self.measurement_file_1 = Path(self.test_workspace, self.default_test_file)
        self.measurement_file_2 = Path(self.test_workspace, self.class_test_file)
        self.saved_file = Path(self.test_workspace, self.id().split(".")[-1] + ".mf4")

        self.setUpBatchWidget(measurement_files=[str(self.measurement_file_1), str(self.measurement_file_2)])
        self.widget.aspects.setCurrentIndex(self.stack_aspect)

    def test_PushButton_Stack(self):
        """
        Events:
            - Press PushButton "Stack"
            - Save measurement file

        Evaluate:
            - New file is created
            - All channels from both files is available in new created file
        """
        # Expected values
        expected_channels = set()

        with self.OpenMDF(self.measurement_file_1) as mdf_file:
            expected_channels |= set(mdf_file.channels_db)

        with self.OpenMDF(self.measurement_file_2) as mdf_file:
            expected_channels |= set(mdf_file.channels_db)

        # Event
        with mock.patch("asammdf.gui.widgets.batch.QtWidgets.QFileDialog.getSaveFileName") as mo_getSaveFileName:
            mo_getSaveFileName.return_value = str(self.saved_file), ""
            QtTest.QTest.mouseClick(self.widget.stack_btn, QtCore.Qt.MouseButton.LeftButton)
        # Let progress bar finish
        self.processEvents(1)

        # Evaluate
        self.assertTrue(self.saved_file.exists())

        # Evaluate saved file
        with self.OpenMDF(self.saved_file) as mdf_file:
            self.assertTrue(len(expected_channels - set(mdf_file.channels_db)) == 0)
