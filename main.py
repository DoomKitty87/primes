import time
import math
import sys
import random
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QComboBox, QGridLayout, QMainWindow, QStatusBar, QToolBar, QPushButton, QLineEdit, QCheckBox
from PyQt6.QtGui import QIntValidator

#def prepare_command():
#  tocompute = input("How many primes would you like to compute?: ")
#  n = ''
#  for i in tocompute:
#    if (i.isdigit()):
#      n += i
#  tocompute = n
#  return int(tocompute)

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
    primes = list(filter(self.is_prime_simple, range(1, num)))
    end = time.time()
    elapsed = end - start
    return (primes)
    print('Finished in', elapsed, 'seconds.')

  def run_eratosthenes(self, num):
    start = time.time()
    primes = self.sieve_of_eratosthenes(num)
    end = time.time()
    elapsed = end - start
    return (primes)
    print('Finished in', elapsed, 'seconds.')

  def run_atkin(self, num):
    start = time.time()
    start_cpu = time.process_time()
    primes = self.sieve_of_atkin(num)
    end = time.time()
    end_cpu = time.process_time()
    elapsed = end - start
    elapsed_cpu = end_cpu - start_cpu
    return primes
    print('Finished in', elapsed, 'seconds.')
    print('Used', elapsed_cpu, 'seconds of cpu time.')

  def run_atkin_optimized(self, num):
    start = time.time()
    start_cpu = time.process_time()
    primes = self.atkin_optimized(num)
    end = time.time()
    end_cpu = time.process_time()
    elapsed = end - start
    elapsed_cpu = end_cpu - start_cpu
    return (primes)
    print('Finished in', elapsed, 'seconds.')
    print('Used', elapsed_cpu, 'seconds of cpu time.')

class MainWidget(QWidget):
  def __init__(self, parent):
    super().__init__(parent=parent)
    self.label = QLabel("Run prime generator")
    self.run_button = QPushButton("Run primes")
    self.run_button.clicked.connect(parent.runPrimes)
    self.type_select = QComboBox();
    self.mode_select = QComboBox();
    self.type_select.addItems(["Simple", "Eratosthenes", "Atkin", "Atkin-Optimized"])
    self.mode_select.addItems(["Primes"])
    self.primes_count = QLineEdit()
    self.primes_count.setValidator(QIntValidator())
    self.file_output = QCheckBox("Output to text file?")
    self.output_text = QLabel()

    self.output_list = QLabel()
    self.layout = QGridLayout()
    self.layout.addWidget(self.label, 1, 0)
    self.layout.addWidget(self.run_button, 2, 0)
    self.layout.addWidget(self.type_select, 3, 0)
    self.layout.addWidget(self.mode_select, 4, 0)
    self.layout.addWidget(self.primes_count, 5, 0)
    self.layout.addWidget(self.file_output, 6, 0)
    self.layout.addWidget(self.output_text, 7, 0)
    self.layout.addWidget(self.output_list, 1, 1, 25, 1)
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
    num = (int)(self.main_widget.primes_count.text())
    match self.main_widget.type_select.currentText():
      case "Atkin":
        output = self.primeCalc.run_atkin(num)
      case "Atkin-Optimized":
        output = self.primeCalc.run_atkin_optimized(num)
      case "Eratosthenes":
        output = self.primeCalc.run_eratosthenes(num)
      case "Simple":
        output = self.primeCalc.run_primecalc_simple(num)
    
    match self.main_widget.mode_select.currentText():
      case "Primes":
        pass
    self.main_widget.output_text.clear()
    self.primesCalculated += len(output)
    self.statusBar().showMessage(f"Primes Calculated: {self.primesCalculated}")
    self.main_widget.output_text.setText(f"Largest prime found: {output[len(output) - 1]}")
    strout = ""
    for i in range(1, 25):
      strout += str(output[random.randint(0, len(output) - 1)])
      strout += "\n"
    self.main_widget.output_list.setText(strout)
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