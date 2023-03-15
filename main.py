from re import M
import time
import math
import sys
import random
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QComboBox, QGridLayout, QMainWindow, QStatusBar, QToolBar, QPushButton, QLineEdit, QCheckBox
from PyQt6.QtGui import QIntValidator
import json
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class PrimeCalculator():

  def is_prime_simple(self, num):
    for x in range(2, num):
      if num % x == 0:
        return False
    return True

  def sieve_of_eratosthenes(self, num):
    primes = []
    for i in range(2, num + 1):
      primes.append(i)
    i = 2
    while i <= int(math.sqrt(num)):
      if i in primes:
        for j in range(i * 2, num + 1, i):
          if j in primes:
            primes.remove(j)
      i += 1
    return primes

  def sieve_of_atkin(self, num):
    out = []
    if num > 2:
      out.append(2)
    if num > 3:
      out.append(3)

    sieve = [False] * (num + 1)
    for i in range(0, num + 1):
      sieve[i] = False
    x = 1
    while x * x <= num:
      y = 1
      while y * y <= num:
        n = (4 * x * x) + (y * y)
        if (n <= num and (n % 12 == 1 or n % 12 == 5)):
          sieve[n] ^= True
        n = (3 * x * x) + (y * y)
        if n <= num and n % 12 == 7:
          sieve[n] ^= True
        n = (3 * x * x) - (y * y)
        if (x > y and n <= num and n % 12 == 11):
          sieve[n] ^= True
        y += 1
      x += 1
    r = 5
    while r * r <= num:
      if sieve[r]:
        for i in range(r * r, num + 1, r * r):
          sieve[i] = False
      r += 1
    for a in range(5, num + 1):
      if sieve[a]:
        out.append(a)
    return out
  
  def atkin_optimized(self, num):
    P = []
    if num > 2:
      P.append(2)
    if num > 3:
      P.append(3)
    r = range(1, int(math.sqrt(num)) + 1)
    sieve = [False] * (num + 1)
    for x in r:
      for y in r:
        xx = x * x
        yy = y * y
        xx3 = 3 * xx
        n = 4 * xx + yy
        if n < num and (n % 12 == 1 or n % 12 == 5): sieve[n] = not sieve[n]
        n = xx3 + yy
        if n <= num and n % 12 == 7: sieve[n] = not sieve[n]
        n = xx3 - yy
        if x > y and n < num and n % 12 == 11: sieve[n] = not sieve[n]
    for x in range(5, int(math.sqrt(num))):
      if sieve[x]:
        xx = x * x
        for y in range(xx, num + 1, xx):
          sieve[y] = False
    for p in range(5, num):
      if sieve[p]: P.append(p)
    return P

  def run_primecalc_simple(self, num):
    start = time.time()
    start_cpu = time.process_time()
    primes = list(filter(self.is_prime_simple, range(1, num)))
    end = time.time()
    end_cpu = time.process_time()
    elapsed = end - start
    elapsed_cpu = end_cpu - start_cpu
    return (primes, elapsed_cpu)

  def run_eratosthenes(self, num):
    start = time.time()
    start_cpu = time.process_time()
    primes = self.sieve_of_eratosthenes(num)
    end = time.time()
    end_cpu = time.process_time()
    elapsed = end - start
    elapsed_cpu = end_cpu - start_cpu
    return (primes, elapsed_cpu)

  def run_atkin(self, num):
    start = time.time()
    start_cpu = time.process_time()
    primes = self.sieve_of_atkin(num)
    end = time.time()
    end_cpu = time.process_time()
    elapsed = end - start
    elapsed_cpu = end_cpu - start_cpu
    return (primes, elapsed_cpu)

  def run_atkin_optimized(self, num):
    start = time.time()
    start_cpu = time.process_time()
    primes = self.atkin_optimized(num)
    end = time.time()
    end_cpu = time.process_time()
    elapsed = end - start
    elapsed_cpu = end_cpu - start_cpu
    return (primes, elapsed_cpu)

  def lucas_lehmer(self, num):
    s = 4
    m = 2 ** p -1
    for _ in range(p - 2):
      s = ((s * s) - 2) % m
    return s == 0

class MainWidget(QWidget):
  def __init__(self, parent):
    super().__init__(parent=parent)
    self.label = QLabel("Run prime generator")
    self.run_button = QPushButton("Run primes")
    self.run_button.clicked.connect(parent.runPrimes)
    self.type_select = QComboBox();
    self.mode_select = QComboBox();
    self.type_select.addItems(["Simple", "Eratosthenes", "Atkin", "Atkin-Optimized"])
    self.mode_select.addItems(["Primes", "Mersenne"])
    self.primes_count = QLineEdit()
    self.primes_count.setValidator(QIntValidator())
    self.file_output = QCheckBox("Output to text file?")
    self.stats_output = QCheckBox("Save run statistics?")
    self.output_text = QLabel()
    self.past_stats = QLabel()

    self.range_start = QLineEdit()
    self.range_end = QLineEdit()
    self.range_start.setValidator(QIntValidator())
    self.range_start.setPlaceholderText("Start (inclusive)")
    self.range_end.setValidator(QIntValidator())
    self.range_end.setPlaceholderText("End (inclusive)")
    self.use_range = QCheckBox("Limit output to range?")

    self.figure = plt.figure()
    self.canvas = FigureCanvas(self.figure)

    self.output_list = QLabel()
    self.layout = QGridLayout()
    self.layout.addWidget(self.label, 1, 0)
    self.layout.addWidget(self.run_button, 2, 0)
    self.layout.addWidget(self.type_select, 3, 0)
    self.layout.addWidget(self.mode_select, 4, 0)
    self.layout.addWidget(self.primes_count, 5, 0)
    self.layout.addWidget(self.file_output, 6, 0)
    self.layout.addWidget(self.stats_output, 7, 0)
    self.layout.addWidget(self.output_text, 8, 0)
    self.layout.addWidget(self.use_range, 9, 0)
    self.layout.addWidget(self.range_start, 10, 0)
    self.layout.addWidget(self.range_end, 11, 0)
    self.layout.addWidget(self.output_list, 1, 1, 25, 1)
    self.layout.addWidget(self.past_stats, 1, 2, 10, 1)
    self.layout.addWidget(self.output_list, 1, 3, 5, 1)
    self.layout.addWidget(self.canvas, 1, 4, 10, 1)
    self.setLayout(self.layout)

class Window(QMainWindow):
  def __init__(self):
    super().__init__(parent=None)
    self.setWindowTitle("Fun With Primes")

    self.main_widget = MainWidget(self)
    self.setCentralWidget(self.main_widget)
    self._createMenu()
    self._createToolBar()
    self._createStatusBar()
    self.primeCalc = PrimeCalculator()
    self.primesCalculated = 0
    self.cpuTotal = 0

    try:
      with open("primesavedstats.json", "r") as f:
        dat = json.loads(f.read())
      displaystr = []
      plotdat = []
      i = 0
      for obj in reversed(dat):
        if (i >= 15): break
        plotdat.append(obj)
        displaystr.append(str(obj["date"]) + " Primes: " + str(obj["primes"]) + " Method: " + obj["computemethod"] + " Cpu Time: " + str(round(obj["cputime"], 3)))
        i += 1
      self.main_widget.past_stats.setText("\n".join(displaystr))
      self.main_widget.figure.clear()
      ax = self.main_widget.figure.add_subplot()
      c = 0
      colors = ['tab:blue', 'tab:orange', 'tab:gray', 'tab:olive']
      greatest = 0
      yticks = []
      yticklabels = []
      for _type in [self.main_widget.type_select.itemText(i) for i in range(self.main_widget.type_select.count())]:
        _ax = ax.twinx()
        _ax.set_yscale("log")
        xvals = [x["cputime"] for x in plotdat if x["computemethod"] == _type]
        yvals = [x["primes"] for x in plotdat if x["computemethod"] == _type]
        xvals.sort()
        yvals.sort()
        _ax.plot(xvals, yvals, '*-', color=colors[c])
        if yvals[-1:] != []:
          if yvals[-1] > greatest:
            yticks = _ax.get_yticks() 
            yticklabels = _ax.get_yticklabels()
            greatest = yvals[-1]
        _ax.set_yticks([])
        _ax.set_yticklabels([])
        _ax.spines[['right', 'top']].set_visible(False)
        _ax.tick_params('both', bottom=False, top=False, right=False, left=False)
        c += 1
      ax.set_yscale("log")
      ax.set_yticks(yticks)
      ax.set_yticklabels(yticklabels)
      ax.spines[['right', 'top']].set_visible(False)
      ax.tick_params('both', bottom=True, left=True, top=False, right=False)
      self.main_widget.canvas.draw()
    except:
      self.main_widget.past_stats.setText("No saved statistics")
      pass

  def _createMenu(self):
    menu = self.menuBar().addMenu("&Menu")
    menu.addAction("&Exit", self.close)

  def _createToolBar(self):
    tools = QToolBar()
    tools.addAction("Exit", self.close)
    self.addToolBar(tools)

  def _createStatusBar(self):
    status = QStatusBar()
    status.showMessage("Primes Calculated: 0")
    self.setStatusBar(status)

  def runPrimes(self):
    try: num = (int)(self.main_widget.primes_count.text())
    except: return
    if self.main_widget.type_select.currentText() == "Atkin":
      cputemeth = "Atkin"
      output = self.primeCalc.run_atkin(num)
      cpu = output[1]
      output = output[0]
    elif self.main_widget.type_select.currentText() == "Atkin-Optimized":
      cputemeth = "Atkin-Optimized"
      output = self.primeCalc.run_atkin_optimized(num)
      cpu = output[1]
      output = output[0]
    elif self.main_widget.type_select.currentText() == "Eratosthenes":
      cputemeth = "Eratosthenes"
      output = self.primeCalc.run_eratosthenes(num)
      cpu = output[1]
      output = output[0]
    elif self.main_widget.type_select.currentText() == "Simple":
      cputemeth = "Simple"
      output = self.primeCalc.run_primecalc_simple(num)
      cpu = output[1]
      output = output[0]
    
    if self.main_widget.mode_select.currentText() == "Primes":
      pass
    elif self.main_widget.mode_select.currentText() == "Mersenne":


      newout = []
      for n in output[:]:
        for i in output[:]:
          if n == 2 ** i - 1:
            newout.append(n)
      output = newout
    
    if self.main_widget.use_range.isChecked() and int(self.main_widget.range_start.text()) < int(self.main_widget.range_end.text()):
      if self.main_widget.range_start.text() != '':
        for n in output[:]:
          if n < int(self.main_widget.range_start.text()):
            output.remove(n)
      if self.main_widget.range_end.text() != '':
        for n in output[:]:
          if n > int(self.main_widget.range_end.text()):
            output.remove(n)
    
    self.main_widget.output_text.clear()
    self.primesCalculated += len(output)
    self.cpuTotal += cpu
    self.statusBar().showMessage(f"Primes Calculated: {self.primesCalculated}, Total Cpu Time Used: {self.cpuTotal}")
    try:
      self.main_widget.output_text.setText(f"Largest prime found: {output[len(output) - 1]}")
    except:
      pass
    strout = ""
    try:
      for i in range(1, 25):
        strout += str(output[random.randint(0, len(output) - 1)])
        strout += "\n"
    except:
      pass
    self.main_widget.output_list.setText(strout)
    if self.main_widget.stats_output.isChecked():
      try:
        f = open("primesavedstats.json", "r")
      except:
        f = open("primesavedstats.json", "w")
        f.close()
        f = open("primesavedstats.json", "r")
      try:
        dat = json.loads(f.read())
      except:
        dat = []
      f.close()
      
      dat.append({
        "date": time.time(),
        "primes": len(output),
        "computemethod": cputemeth,
        "cputime": cpu
      })
      with open("primesavedstats.json", "w") as f: f.write(json.dumps(dat, indent=2))
      with open("primesavedstats.json", "r") as f:
        dat = json.loads(f.read())
      displaystr = []
      plotdat = []
      i = 0
      for obj in reversed(dat):
        if (i >= 15): break
        plotdat.append(obj)
        displaystr.append(str(obj["date"]) + " Primes: " + str(obj["primes"]) + " Method: " + obj["computemethod"] + " Cpu Time: " + str(round(obj["cputime"], 3)))
        i += 1
      self.main_widget.past_stats.setText("\n".join(displaystr))
      self.main_widget.figure.clear()
      ax = self.main_widget.figure.add_subplot()
      c = 0
      colors = ['tab:blue', 'tab:orange', 'tab:gray', 'tab:olive']
      greatest = 0
      yticks = []
      yticklabels = []
      for _type in [self.main_widget.type_select.itemText(i) for i in range(self.main_widget.type_select.count())]:
        _ax = ax.twinx()
        _ax.set_yscale("log")
        xvals = [x["cputime"] for x in plotdat if x["computemethod"] == _type]
        yvals = [x["primes"] for x in plotdat if x["computemethod"] == _type]
        xvals.sort()
        yvals.sort()
        _ax.plot(xvals, yvals, '*-', color=colors[c])
        if yvals[-1:] != []:
          if yvals[-1] > greatest:
            yticks = _ax.get_yticks()
            yticklabels = _ax.get_yticklabels()
            greatest = yvals[-1]
        _ax.set_yticks([])
        _ax.set_yticklabels([])
        _ax.spines[['right', 'top']].set_visible(False)
        _ax.tick_params('both', bottom=False, top=False, right=False, left=False)
        c += 1
      ax.set_yscale("log")
      ax.set_yticks(yticks)
      ax.set_yticklabels(yticklabels)
      ax.spines[['right', 'top']].set_visible(False)
      ax.tick_params('both', bottom=True, left=True, top=False, right=False)
      self.main_widget.canvas.draw()
    
    if self.main_widget.file_output.isChecked():
      created = False
      i = 0
      f = None
      while created is not True:
        try:
          f = open(f"primesoutput{i}.txt", "x")
          created = True
        except:
          pass
        i += 1
      f.write('\n'.join([str(x) for x in output]))
      f.close()

if __name__ == "__main__":
  app = QApplication([])
  window = Window()
  window.show()
  sys.exit(app.exec())