import sys
import traceback
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('WXagg')
import pygame
import pyghelpers
import sympy

from ExcleMagr import ExcelMgr
from checkbox import *
from EventPyghelpers import textAnswerDialogEventProgressing
from TableViewer.Table import WindowListViewer


class Message_window:
    """
    a class that is used to show messages.
    #using tkinter and pygame(maybe)
    """


    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # 隐藏tkinter窗口
        self.YES_NO = 0
        self.RETRY_CANCEL = 1
        self.OK_CANCEL = 2
        self.QUESTION = 3
        self.YES_NO_CANCEL = 4

    def warning(self, message='Warning', title='WARNING'):
        """
        :param title:
        :param message:
        """
        self.root.withdraw()  # 隐藏tkinter窗口
        messagebox.showwarning(title=title, message=message)

    def error(self, message, title='ERROR'):
        """
        :param title:
        :param message:
        """
        self.root.withdraw()  # 隐藏tkinter窗口
        messagebox.showerror(title=title, message=message)

    def browser(self, title="open a file", types=None, caption="C:\\"):
        """

        :param title:
        :param types:
        :param caption:
        """
        self.root.withdraw()  # 隐藏tkinter窗口
        if types is None:
            types = [('ALL', '*')]
        self.select_file(title, types, caption)

    def select_file(self, title="open a file", types=None, dir='C\\:'):
        """

        :param title:
        :param types:
        :param dir:
        """
        if types is None:
            types = [('all', '*')]

        self.root.withdraw()  # 隐藏tkinter窗口
        self.file_name = filedialog.askopenfilename(title=title, filetypes=types, initialdir=dir)  # 显示文件选择对话框

    def question(self, title='QUESTION', question='Question', type=None):
        """

        :param title:
        :param question:
        :param type:
        :return:
        """
        self.root.withdraw()  # 隐藏tkinter窗口
        if type is None:
            type = self.YES_NO
        if type == self.YES_NO:
            answer = messagebox.askyesno(title, question)
        elif type == self.OK_CANCEL:
            answer = messagebox.askokcancel(title, question)
        elif type == self.RETRY_CANCEL:
            answer = messagebox.askretrycancel(title, question)
        elif type == self.QUESTION:
            answer = messagebox.askquestion(title, question)
        elif type == self.YES_NO_CANCEL:
            answer = messagebox.askyesnocancel(title, question)
        else:
            raise TypeError("No matching types!!!")
        return answer

    def get_file_name(self):
        """

        :return: str
        """
        try:
            return self.file_name
        except Exception:
            return None

    def message(self, title='MESSAGE', message='Message'):
        """

        :param title:
        :param message:
        """
        self.root.withdraw()  # 隐藏tkinter窗口
        messagebox.showinfo(title, message)


message_window = Message_window()


def charting(type, mul=False, fig=None, num=1, max=1, pie_pct='%1.2f%%',**all_values):
    """
    :param pie_pct:
    :param type:
    :param fig:
    :param num:
    :param mul:
    :param all_values:
        pie:  <x,labels,colours=None>;
        hist: <x,density=False>;
        box:  <x -> 2d array,notch ->bool=False>;
        violin: <data -> array>;
        error bar: <x,y>;
        hist2d: <x,y,num=100>;
        hexbin: <x,y,num=100>;
        plot: <x,y>
        scatter: <x,y>
    """
    if mul:
        if len(sympy.divisors(max)) > 2:
            lcm = sympy.divisors(max)[-2]
        else:
            lcm = sympy.divisors(max)[0]
        x = max // lcm
        if x > max // x:
            y = max // x
        else:
            x = max // x
            y = max // x
        if type not in ['hist', 'violin', 'hexbin', 'box', 'error bar', 'hist2d', 'pie', 'plot', 'scatter']:
            raise TypeError("'" + str(
                type) + "' is not in available types :'hist','violin','hexbin','box','error bar','hist2d','pie','scatter'\n")
        print(x, y, num)
        plot = fig.add_subplot(x, y, num)
        if type == 'pie':
            if len(all_values) == 2:
                plot.pie(all_values['x'], labels=all_values['labels'], autopct=(pie_pct))
            else:
                plot.pie(all_values['x'], labels=all_values['labels'], colors=all_values['colours'], autopct=pie_pct)
        elif type == 'box':
            if len(all_values) == 1:
                plot.boxplot(all_values['x'])
            else:
                plot.boxplot(all_values['x'], notch=all_values['notch'])
        elif type == 'hist':
            if len(all_values) == 1:
                plot.hist(all_values['x'])
            else:
                plot.hist(all_values['x'], density=all_values['density'])
        elif type == 'violin':
            plot.violinplot(all_values['data'])
        elif type == 'error bar':
            plot.errorbar(all_values['x'], all_values['y'])
        elif type == 'hist2d':
            if len(all_values) == 2:
                plot.hist2d(all_values['x'], all_values['y'], 100, cmap='Blues')
            else:
                plot.hist2d(all_values['x'], all_values['y'], all_values['number'], cmap='Blues')
        elif type == 'hexbin':
            if len(all_values) == 2:
                plot.hexbin(all_values['x'], all_values['y'], cmap='Blues')
            else:
                plot.hexbin(all_values['x'], all_values['y'], cmap='Blues', gridsize=all_values['number'])
        elif type == "plot":
            plot.plot(all_values['x'], all_values['y'])
        elif type == 'scatter':
            plot.scatter(all_values['x'], all_values['y'])
    else:
        if type not in ['hist', 'violin', 'hexbin', 'box', 'error bar', 'hist2d', 'pie', 'plot', 'scatter']:
            raise TypeError("'" + str(
                type) + "' is not in available types :'hist','violin','hexbin','box','error bar','hist2d','pie','plot','scatter'\n")
        if type == 'pie':
            if len(all_values) == 2:
                plt.pie(all_values['x'], labels=all_values['labels'], autopct=pie_pct)
                plt.show()
            else:
                plt.pie(all_values['x'], labels=all_values['labels'], colors=all_values['colours'], autopct=pie_pct)
                plt.show()
        elif type == 'box':
            if len(all_values) == 1:
                plt.boxplot(all_values['x'])
                plt.show()
            else:
                plt.boxplot(all_values['x'], notch=all_values['notch'])
                plt.show()
        elif type == 'hist':
            if len(all_values) == 1:
                plt.hist(all_values['x'])
                plt.show()
            else:
                plt.hist(all_values['x'], density=all_values['density'])
                plt.show()
        elif type == 'violin':
            plt.violinplot(all_values['data'])
            plt.show()
        elif type == 'error bar':
            plt.errorbar(all_values['x'], all_values['y'])
            plt.show()
        elif type == 'hist2d':
            if len(all_values) == 2:
                plt.hist2d(all_values['x'], all_values['y'], 100, cmap='Blues')
            else:
                plt.hist2d(all_values['x'], all_values['y'], all_values['number'], cmap='Blues')
            plt.show()
        elif type == 'hexbin':
            if len(all_values) == 2:
                plt.hexbin(all_values['x'], all_values['y'], cmap='Blues')
                plt.show()
            else:
                plt.hexbin(all_values['x'], all_values['y'], cmap='Blues', gridsize=all_values['number'])
                plt.show()
        elif type == "plot":
            plt.plot(all_values['x'], all_values['y'])
            plt.show()
        elif type == 'scatter':
            plt.scatter(all_values['x'], all_values['y'])
            plt.show()


def charts(window, clock, choices, **all_values):
    """

    :param window:
    :param clock:
    :param choices:
    :param all_values:
    """
    fig = plt.figure()
    try:
        xs = all_values['xs']
        ys = all_values['ys']
        one_table = all_values['one_table']
        mult = True
    except KeyError:
        mult = False
    if type(choices) != str and (type(choices) == list or type(choices) == tuple):
        if len(choices) > 0:
            m = choices
            max_num = len(m)
            if not mult:
                for i, j in zip(m, range(len(m))):
                    if i == 0:
                        charting('pie', True, fig, j + 1, max_num, x=all_values['x'], labels=all_values['labels'])
                    elif i == 1:
                        charting('hist', True, fig, j + 1, max_num, x=all_values['x'])
                    elif i == 2:
                        charting('box', True, fig, j + 1, max_num, x=all_values['x'])
                    elif i == 3:
                        charting('violin', True, fig, j + 1, max_num, data=all_values['x'])
                    elif i == 4:
                        charting('error bar', True, fig, j + 1, max_num, x=all_values['x'], y=all_values['y'])
                    elif i == 5:
                        label = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                            'input the number of hist of the each sides', 'OK',
                                                            'CANCEL', backgroundColor=(90, 90, 150),
                                                            promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                        charting('hist2d', True, fig, j + 1, max_num, x=all_values['x'], y=all_values['y'],
                                 number=int(label))
                    elif i == 6:
                        label = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                            'input the number of hex of the each sides', 'OK', 'CANCEL',
                                                            backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                                            inputTextColor=(0, 0, 0))
                        charting('hexbin', True, fig, j + 1, max_num, x=all_values['x'], y=all_values['y'],
                                 number=int(label))
                    elif i == 7:
                        charting('plot', True, fig, j + 1, max_num, x=all_values['x'], y=all_values['y'])

            else:
                x_index = y_index = 0
                for i, j in zip(m, range(len(m))):
                    if i == 0:
                        x = xs[x_index]
                        curr_label = all_values['labels'][j]
                        if one_table:
                            charting('pie', True, fig, j + 1, max_num, x=x, labels=curr_label)
                        else:
                            plt.pie(x, labels=curr_label)
                        x_index += 1
                    elif i == 1:
                        x = xs[x_index]
                        if one_table:
                            charting('hist', True, fig, j + 1, max_num, x=x)
                        else:
                            plt.hist(x)
                        x_index += 1
                    elif i == 2:
                        x = xs[x_index]
                        if one_table:
                            charting('box', True, fig, j + 1, max_num, x=x)
                        else:
                            plt.boxplot(x)
                        x_index += 1
                    elif i == 3:
                        x = xs[x_index]
                        if one_table:
                            charting('violin', True, fig, j + 1, max_num, data=x)
                        else:
                            plt.violinplot(x)
                        x_index += 1
                    elif i == 4:
                        x = xs[x_index]
                        y = ys[y_index]
                        if one_table:
                            charting('error bar', True, fig, j + 1, max_num, x=x, y=y)
                        else:
                            plt.errorbar(x, y)
                        x_index += 1
                        y_index += 1
                    elif i == 5:
                        x = xs[x_index]
                        y = ys[y_index]
                        number = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                             'input the number of hist of the each sides', 'OK',
                                                             'CANCEL', backgroundColor=(90, 90, 150),
                                                             promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                        if one_table:
                            charting('hist2d', True, fig, j + 1, max_num, x=x, y=y,
                                     number=int(number))
                        else:
                            plt.hist2d(x, y, int(number))
                        x_index += 1
                        y_index += 1
                    elif i == 6:
                        x = xs[x_index]
                        y = ys[y_index]
                        number = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                             'input the number of hex of the each sides', 'OK',
                                                             'CANCEL', backgroundColor=(90, 90, 150),
                                                             promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                        if one_table:
                            charting('hexbin', True, fig, j + 1, max_num, x=x, y=y, number=int(number))
                        else:
                            plt.hexbin(x, y, gridsize=int(number))
                        x_index += 1
                        y_index += 1
                    elif i == 7:
                        x = xs[x_index]
                        y = ys[y_index]
                        if one_table:
                            charting('plot', True, fig, j + 1, max_num, x=x, y=y)
                        else:
                            plt.plot(x, y)
                        x_index += 1
                        y_index += 1
                    elif i == 8:
                        x = xs[x_index]
                        y = ys[y_index]
                        if one_table:
                            charting('scatter', True, fig, j + 1, max_num, x=x, y=y)
                        else:
                            plt.scatter(x, y)
                        x_index += 1
                        y_index += 1

            plt.show()
        else:
            if choices[0] == 0:
                charting('pie', x=all_values['x'], labels=all_values['labels'])
            elif choices[0] == 1:
                charting('hist', x=all_values['x'])
            elif choices[0] == 2:
                charting('box', x=all_values['x'])
            elif choices[0] == 3:
                charting('violin', data=all_values['x'])
            elif choices[0] == 4:
                charting('error bar', x=all_values['x'], y=all_values['y'])
            elif choices[0] == 5:
                label = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                    'input the number of hex of the each sides', 'OK', 'CANCEL',
                                                    backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                                    inputTextColor=(0, 0, 0))
                try:
                    charting('hist2d', x=all_values['x'], y=all_values['y'], number=int(label))
                except:
                    charting('hist2d', x=all_values['x'], y=all_values['y'], number=30)
            elif choices[0] == 6:
                label = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                    'input the number of hex of the each sides', 'OK', 'CANCEL',
                                                    backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                                    inputTextColor=(0, 0, 0))
                charting('hexbin', x=all_values['x'], y=all_values['y'], number=int(label))
            elif choices[0] == 7:
                charting('hexbin', x=all_values['x'], y=all_values['y'])
            elif choices[0] == 8:
                charting('scatter', x=all_values['x'], y=all_values['y'])
    elif type(choices) == int:
        if choices == 0:
            charting('pie', x=all_values['x'], labels=all_values['labels'])
        elif choices == 1:
            charting('hist', x=all_values['x'])
        elif choices == 2:
            charting('box', x=all_values['x'])
        elif choices == 3:
            charting('violin', data=all_values['x'])
        elif choices == 4:
            charting('error bar', x=all_values['x'], y=all_values['y'])
        elif choices == 5:
            label = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                'input the number of hex of the each sides', 'OK', 'CANCEL',
                                                backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                                inputTextColor=(0, 0, 0))
            charting('hist2d', x=all_values['x'], y=all_values['y'], number=int(label))
        elif choices == 6:
            label = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                'input the number of hex of the each sides', 'OK', 'CANCEL',
                                                backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                                inputTextColor=(0, 0, 0))
            charting('hexbin', x=all_values['x'], y=all_values['y'], number=int(label))
        elif choices == 7:
            charting('plot', x=all_values['x'], y=all_values['y'])
        elif choices == 8:
            charting('scatter', x=all_values['x'], y=all_values['y'])


def load_label(window, num):
    """

    :param window:
    :param num:
    :return:
    """
    global message_window
    message_window.browser("Choose an Excel file for the label's source", [('EXCEL files', '.xlsx')])
    file_name = message_window.file_name
    if file_name == '':
        message_window.error("failed to process because of empty file name")
        return
    choice = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300), 'how do you want to collect label',
                                        "by line(----)", 'by column(| | |)')
    file = ExcelMgr(file_name)
    file_data = file.data
    if not choice:
        col = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200), 'input column number(starts with 0)', 'OK',
                                          'CANCEL',
                                          backgroundColor=(90, 90, 150),
                                          promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
        try:
            col_num = int(col)
        except TypeError:
            if col is not None:
                message_window.error('bad inputs for int ' + str(col))
            return
        cols_start = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                 'input cols start position of arrange (starts with 0)', 'OK',
                                                 'CANCEL', backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                                 inputTextColor=(0, 0, 0))
        try:
            col_start_num = int(cols_start)
        except TypeError:
            if cols_start is not None:
                message_window.error('bad inputs for int ' + str(cols_start))
            return
        cols_end = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                               'input cols end position of arrange(include)', 'OK', 'CANCEL',
                                               backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                               inputTextColor=(0, 0, 0))
        try:
            col_end_num = int(cols_end)
        except TypeError:
            if cols_end is not None:
                message_window.error('bad inputs for int ' + str(cols_end))
            return
        try:
            data = file_data
            data = [line_[col_num] for line_ in data]
            data = data[col_start_num:col_end_num + 1]
            if len(data) > num:
                message_window.warning("too many labels!!! we will cut to the right number")
                labels = data[0:num]
            elif len(data) == 0:
                message_window.error("no labels has chosen")
                return
            elif len(data) < num:
                message_window.error("too less labels!! function ends")
                return
            else:
                labels = data
            return labels
        except Exception as e:
            message_window.error(str(e))
            return
    else:
        line = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200), 'input line number(starts with 0)', 'OK',
                                           'CANCEL',
                                           backgroundColor=(90, 90, 150),
                                           promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
        try:
            line_num = int(line)
        except TypeError:
            if line is not None:
                message_window.error('bad inputs for int ' + str(line))
            return
        line_start = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                 'input arrange start position of line (starts with 0)' + str(
                                                     line_num), 'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                 promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
        try:
            line_start_num = int(line_start)
        except TypeError:
            if line_start is not None:
                message_window.error('bad inputs for int ' + str(line_start))
            return
        line_end = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                               'input end position of line ' + str(line_num),
                                               'OK', 'CANCEL', backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                               inputTextColor=(0, 0, 0))
        try:
            line_end_num = int(line_end)
        except TypeError:
            if line_end is not None:
                message_window.error('bad inputs for int ' + str(line_end))
            return
        try:
            num = 0
            data = file_data[line_num]
            data = data[line_start_num:line_end_num + 1]
        except IndexError as e:
            message_window.error(str(e))
            return
        if len(data) > num:
            message_window.warning("too many labels!!! we will cut to the right number")
            labels = data[0:num]
        elif len(data) < num:
            message_window.error("too less labels!! function ends")
            return
        elif len(data) == 0:
            message_window.error("no labels has chosen")
            return
        else:
            labels = data
        return labels


def data_charter(window, clock, debug=False):
    """
    version:3.1
    develop time:2025-1-17
    """
    global message_window
    data_collecting_method = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300), 'how do you want to collect data',
                                        '.xlsx file', "by inputting the data manually")
    mult = pyghelpers.textYesNoDialog(window, (0, 300, 600, 300), 'you want to draw chart(s) on',
                                      'multiple separate chart tables', "one signal chart table")
    pie = False
    if mult:
        diff_source = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                 'you want to select the data for charts from',
                                                 'multiple .xlsx files', "one signal .xlsx file")

    if data_collecting_method:  #################################################  load from excel files ###########################################################################

        message_window.browser("Choose an Excel file for the data's source", [('EXCEL files', '.xlsx')])
        file_name = message_window.file_name
        if mult:
            one_chart = False
        else:
            one_chart = True
        if file_name == '':
            message_window.error("failed to process because of empty file name")
            return
        try:
            file = ExcelMgr(file_name)
            file_data = file.data
            a = CheckBox(9, ['pie', 'hist', 'box', 'violin', 'error bar', 'hist2d', 'hexbin', 'plot', 'scatter'], 9,
                         window, clock, first_x=40, first_y=100, each_add_x=0, each_add_y=30)
            list_preview = WindowListViewer(file_data, (1004, 410), window, (0, 200))
            if type(a.clicked_choices) == str:
                return
            elif len(a.clicked_choices) == 0:
                choice_ = message_window.question("you didn't choice any type of charts, do you want to exit?")
                if not choice_:
                    return data_charter(window, clock)
                else:
                    return
            if mult:
                diff_file_source = diff_source
            else:
                diff_file_source = False
            choice = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300), 'how do you want to collect data',
                                                "by line(----)", 'by column(| | |)')
            if not mult:
                xs = ys = []
                pie = False
            choices = a.clicked_choices
            pie_labels = []
            pie_value_poses = []
            chart_choices = []
            for a in a.clicked_choices:
                num = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200), 'How many '+['pie', 'hist', 'box', 'violin', 'error bar', 'hist2d', 'hexbin', 'plot', 'scatter'][a]+' charts do you want to draw?',
                                                              'OK',
                                                              'CANCEL', backgroundColor=(90, 90, 150),
                                                              promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                try:
                    num = int(num)
                except Exception:
                    message_window.error("Can't turn "+str(num)+' into an integer')
                    return
                if num < 0:
                    message_window.error("You can't draw negative charts!")
                    return
                else:
                    for i in range(num):
                        chart_choices.append(a)

            for a, j in zip(chart_choices, range(len(chart_choices))):
                if type(a) is str:
                    break
                if j >= 1 and diff_file_source:
                    message_window.browser("Choose an Excel file for the data's source for " +
                                           ['pie', 'hist', 'box', 'violin', 'error bar', 'hist2d', 'hexbin', 'plot',
                                            'scatter'][a], [('EXCEL files', '.xlsx')])
                    file_name = message_window.file_name
                    if file_name is None:
                        message_window.error("failed to process because of empty file name")
                        return
                    file = ExcelMgr(file_name)
                    file_data = file.data
                if not choice:####by column
                    if a <= 3:
                        arrange = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200), 'input arrange number',
                                                              [list_preview.draw],[list_preview.handle_event],'OK',
                                                              'CANCEL', backgroundColor=(90, 90, 150),
                                                              promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                        try:
                            arrange_num = int(arrange)
                        except TypeError:
                            if arrange is not None:
                                message_window.error('bad inputs for int ' + str(arrange))
                            return
                        cols_start = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                 'input cols start position of arrange (starts with 0)' + str(
                                                                     arrange_num), [list_preview.draw],[list_preview.handle_event],'OK',
                                                                 'CANCEL', backgroundColor=(90, 90, 150),
                                                                 promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                        try:
                            col_start_num = int(cols_start)
                        except TypeError:
                            if cols_start is not None:
                                message_window.error('bad inputs for int ' + str(cols_start))
                            return
                        cols_end = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                               'input cols end position of arrange (include)' + str(
                                                                   arrange_num),
                                                               [list_preview.draw],[list_preview.handle_event],'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                               promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                        try:
                            col_end_num = int(cols_end)
                        except TypeError:
                            if cols_end is not None:
                                message_window.error('bad inputs for int ' + str(cols_end))
                            return
                        try:
                            data = []
                            num = 0
                            avail_num = 0
                            for i in file_data[col_start_num - 1:col_end_num]:
                                if type(i[arrange_num - 1]) not in [int, float]:
                                    pass

                                else:
                                    avail_num += 1
                                    data.append(i[arrange_num - 1])
                                num += 1
                            if avail_num != num:
                                message_window.warning('we found ' + str(
                                    num - avail_num) + ' valid data(s) in your file,we will ignore them(it)')
                            if len(data) == 0:
                                message_window.error('Exit because of no available data')
                                return
                        except IndexError as e:
                            message_window.error(str(e))
                            return
                        if a == 0:  # pie chart needs user to input labels
                            if mult:
                                pie = True
                            label_choice = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                                      'please input the labels ',
                                                                      "manually", 'automatically create')
                            if label_choice:
                                label = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                    "input you labels split each other with ';'"+'(number:' + str(
                                                                        len(data)) + '),input none to set labels automatically',
                                                                    [list_preview.draw],[list_preview.handle_event],'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                                    promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                                if label is not None:
                                    label = label.split(";")
                                    if len(label) > len(data):
                                        message_window.warning(
                                            "label's num (" + str(len(label)) + ", is higher than data's num (" + str(
                                                len(data))
                                            + ",system will adjust this by adding labels automatically")
                                        label = label[:len(data)]
                                    elif len(label) < len(data):
                                        message_window.warning(
                                            "label's num (" + str(len(label)) + ", is lower than data's num (" + str(
                                                len(data)) + ',system will adjust this by adding labels automatically')
                                        k = len(label)
                                        label = label + ['label ' + str(k + a) for a in range(len(data) - len(label))]

                                else:
                                    label = ["label " + str(b + 1) for b in range(len(data))]
                                if mult:
                                    charts(window, clock, a, x=data, labels=label)
                                else:
                                    pie_data_index = len(xs)
                                    xs.append(data)
                                    pie_label = label
                                    pie_labels.append(pie_label)
                                    pie_value_poses.append(pie_data_index)
                            else:
                                label_source = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                                          "please select the labels' source",
                                                                          "Excel files(*.xlsx)", 'automatically create')
                                if label_source:
                                    label = load_label(window, len(data))
                                    if label is None:
                                        message_window.error("FATAL ERROR:failed to load labels;function ends")
                                        return
                                else:
                                    label = ["label " + str(b + 1) for b in range(len(data))]
                                    if mult:
                                        charts(window, clock, a, x=data, labels=label)
                                    else:
                                        pie_data_index = len(xs)
                                        xs.append(data)
                                        pie_value_poses.append(pie_data_index)
                                        pie_label = label
                                        pie_labels.append(pie_label)

                        else:
                            if mult:
                                charts(window, clock, a, x=data)
                            else:
                                xs.append(data)
                    else:  # types likes hexbin,hist2d and error bar ||#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
                        arrange = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                              'input arrange number', [list_preview.draw],[list_preview.handle_event],'OK',
                                                              'CANCEL', backgroundColor=(90, 90, 150),
                                                              promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                        try:
                            arrange_num = int(arrange)
                        except TypeError:
                            if arrange is not None:
                                message_window.error('bad inputs for int ' + str(arrange))
                            return
                        cols_start = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                 'input cols start position of arrange (start with 0)' + str(
                                                                     arrange_num), [list_preview.draw],[list_preview.handle_event],'OK',
                                                                 'CANCEL', backgroundColor=(90, 90, 150),
                                                                 promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                        try:
                            col_start_num = int(cols_start)
                        except TypeError:
                            if cols_start is not None:
                                message_window.error('bad inputs for int ' + str(cols_start))
                            return
                        cols_end = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                               'input cols end position of arrange (include)' + str(
                                                                   arrange_num), [list_preview.draw],[list_preview.handle_event],'OK',
                                                               'CANCEL', backgroundColor=(90, 90, 150),
                                                               promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                        try:
                            col_end_num = int(cols_end)
                        except TypeError:
                            if cols_end is not None:
                                message_window.error('bad inputs for int ' + str(cols_end))
                            return
                        try:
                            data = []
                            num = 0
                            avail_num = 0
                            for i in file_data[col_start_num - 1:col_end_num]:
                                if type(i[arrange_num - 1]) not in [int, float]:
                                    pass
                                else:
                                    avail_num += 1
                                    data.append(i[arrange_num - 1])
                                num += 1
                            if avail_num != num:
                                message_window.warning('we found ' + str(
                                    num - avail_num) + ' valid data in your file,we will ignore them')
                        except IndexError as e:
                            message_window.error(str(e))
                            return
                        if a == 4:  # error bar
                            if mult:
                                charts(window, clock, a, x=data)
                            else:
                                xs.append(data)
                        elif a == 5 or a == 6 or a == 7 or a == 8:
                            #  input the 'y' agreement
                            arrange = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200), 'input arrange number',
                                                                  [list_preview.draw],[list_preview.handle_event],'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                                  promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                            try:
                                arrange_num = int(arrange)
                            except TypeError:
                                if arrange is not None:
                                    message_window.error('bad inputs for int ' + str(arrange))
                                return
                            cols_start = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                     'input cols start position of arrange (starts with 0)' + str(
                                                                         arrange_num), [list_preview.draw],[list_preview.handle_event],'OK',
                                                                     'CANCEL', backgroundColor=(90, 90, 150),
                                                                     promptTextColor=(0, 0, 0),
                                                                     inputTextColor=(0, 0, 0))
                            try:
                                col_start_num = int(cols_start)
                            except TypeError:
                                if cols_start is not None:
                                    message_window.error('bad inputs for int ' + str(cols_start))
                                return
                            cols_end = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                   'input cols end position of arrange (include)' + str(
                                                                       arrange_num),
                                                                   [list_preview.draw],[list_preview.handle_event],'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                                   promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                            try:
                                data_y = []
                                num = 0
                                avail_num = 0
                                for i in file_data[col_start_num - 1:col_end_num]:
                                    if type(i[arrange_num - 1]) not in [int, float]:
                                        pass
                                    else:
                                        avail_num += 1
                                        data_y.append(i[arrange_num - 1])
                                    num += 1
                                if avail_num != num:
                                    message_window.warning('we found ' + str(
                                        num - avail_num) + ' valid data in your file,we will ignore them')
                            except IndexError as e:
                                message_window.error(str(e))
                                return
                            if mult:
                                charts(window, clock, a, x=data, y=data_y)
                            else:
                                xs.append(data)
                                ys.append(data_y)

                    #                                       by column (| | |)[end]
######################-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
                else:  # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
######################-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
                    #                                       by line (---)[start]
                    if a <= 3:
                        line = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200), 'input line number', [list_preview.draw]
                                                                ,[list_preview.handle_event],'OK',
                                                           'CANCEL', backgroundColor=(90, 90, 150),
                                                           promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                        try:
                            line_num = int(line)
                        except TypeError:
                            if line is not None:
                                message_window.error('bad inputs for int ' + str(line))
                            return
                        line_start = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                 'input arrange start position("0"means arrange 1) of line ' + str(
                                                                     line_num), [list_preview.draw],[list_preview.handle_event],'OK', 'CANCEL',
                                                                 backgroundColor=(90, 90, 150),
                                                                 promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                        try:
                            line_start_num = int(line_start)
                        except TypeError:
                            if line_start is not None:
                                message_window.error('bad inputs for int ' + str(line_start))
                            return
                        line_end = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                               'input arrange end position of line ' + str(line_num),
                                                               [list_preview.draw],[list_preview.handle_event],'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                               promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                        try:
                            line_end_num = int(line_end)
                        except TypeError:
                            if line_end is not None:
                                message_window.error('bad inputs for int ' + str(line_end))
                            return
                        try:
                            data = []
                            num = 0
                            avail_num = 0
                            data = file_data[line_num]
                            data = data[line_start_num:line_end_num + 1]
                            for i in data:
                                if type(i) not in [int, float]:
                                    pass
                                else:
                                    avail_num += 1
                                num += 1
                            if avail_num != num:
                                message_window.warning('we found ' + str(
                                    num - avail_num) + ' valid data in your file,we will ignore them')
                            if len(data) == 0:
                                return
                        except IndexError as e:
                            message_window.error(str(e))
                            return
                        if a == 0:  # pie chart needs user to input labels
                            label_choice = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                                      'please input the labels ', "manually",
                                                                      'automatically create')
                            pie = True
                            if label_choice:
                                label = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                    "input you labels split each other with ';',(number:" + str(
                                                                        len(data)) + '),input none to set labels automatically',
                                                                    [list_preview.draw],[list_preview.handle_event],'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                                    promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                                if label is not None:
                                    label = label.split(";")
                                    if len(label) > len(data):
                                        message_window.warning(
                                            "label's num (" + str(len(label)) + ", is higher than data's num (" + str(
                                                len(data)) + ",system will adjust this by canceling labels automatically")
                                        label = label[:len(data)]
                                    elif len(label) < len(data):
                                        message_window.warning(
                                            "label's num (" + str(len(label)) + ", is lower than data's num (" + str(
                                                len(data)) + ',system will adjust this by adding labels automatically')
                                        k = len(label)
                                        label = label + ['label ' + str(k + a) for a in range(len(data) - len(label))]

                                else:
                                    label = ["label " + str(b + 1) for b in range(len(data))]
                                if mult:
                                    charts(window, clock, a, x=data, labels=label)
                                else:
                                    pie_value_poses.append(len(xs))
                                    xs.append(data)
                                    pie_label = label
                                    pie_labels.append(pie_label)
                            else:
                                label_source = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                                          "please select the labels' source",
                                                                          "Excel files(*.xlsx)",
                                                                          'automatically create')
                                if label_source:
                                    label = load_label(window, len(data))
                                    if label is None:
                                        message_window.error("FATAL ERROR:failed to load labels;function ends")
                                        return
                                else:
                                    label = ["label " + str(b + 1) for b in range(len(data))]
                                    if mult:
                                        charts(window, clock, a, x=data, labels=label)
                                    else:
                                        pie_value_poses.append(len(xs))
                                        xs.append(data)
                                pie_label = label
                                pie_labels.append(pie_label)
                        else:
                            if mult:
                                charts(window, clock, a, x=data)
                            else:
                                xs.append(data)
                    else:
                        line = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                           'input line number', [list_preview.draw],[list_preview.handle_event],'OK',
                                                           'CANCEL', backgroundColor=(90, 90, 150),
                                                           promptTextColor=(0, 0, 0),
                                                           inputTextColor=(0, 0, 0))
                        try:
                            line_num = int(line)
                        except TypeError:
                            if line is not None:
                                message_window.error('bad inputs for int ' + str(line))
                            return
                        line_start = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                 'input arrange start position of line ' + str(
                                                                     line_num), [list_preview.draw],[list_preview.handle_event],'OK',
                                                                 'CANCEL', backgroundColor=(90, 90, 150),
                                                                 promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                        try:
                            line_start_num = int(line_start)
                        except TypeError:
                            if line_start is not None:
                                message_window.error('bad inputs for int ' + str(line_start))
                            return
                        line_end = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                               'input arrange end position of line ' + str(
                                                                   line_num),
                                                               [list_preview.draw],[list_preview.handle_event],'OK',
                                                               'CANCEL', backgroundColor=(90, 90, 150),
                                                               promptTextColor=(0, 0, 0),
                                                               inputTextColor=(0, 0, 0))
                        try:
                            line_end_num = int(line_end)
                        except TypeError:
                            # app = QApplication(sys.argv)
                            if line_end is not None:
                                message_window.error('bad inputs for int ' + str(line_end))
                            return
                        try:
                            data = []
                            num = 0
                            avail_num = 0
                            data = file_data[line_num]
                            data = data[line_start_num:line_end_num + 1]
                            for i in data:
                                if type(i) not in [int, float]:
                                    pass
                                else:
                                    avail_num += 1
                                num += 1
                            if avail_num != num:
                                message_window.warning('we found ' + str(
                                    num - avail_num) + ' valid data in your file,we will ignore them')
                        except IndexError as e:
                            message_window.error(str(e))
                            return
                        if a == 4:
                            if mult:
                                charts(window, clock, a, x=data)
                            else:
                                xs.append(data)
                        elif a == 5 or a == 6 or a == 7 or a == 8:
                            line = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200), 'input line number for y',
                                                               [list_preview.draw],[list_preview.handle_event],'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                               promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                            try:
                                line_num = int(line)
                            except TypeError:
                                if line is not None:
                                    message_window.error('bad inputs for int ' + str(line))
                                return
                            line_start = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                     'input arrange start position of line ' + str(
                                                                         line_num), [list_preview.draw],[list_preview.handle_event],'OK', 'CANCEL',
                                                                     backgroundColor=(90, 90, 150),
                                                                     promptTextColor=(0, 0, 0),
                                                                     inputTextColor=(0, 0, 0))
                            try:
                                line_start_num = int(line_start)
                            except TypeError:
                                if line_start is not None:
                                    message_window.error('bad inputs for int ' + str(line_start))
                                return
                            line_end = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                                   'input arrange end position of line ' + str(
                                                                       line_num), [list_preview.draw],[list_preview.handle_event],'OK', 'CANCEL',
                                                                   backgroundColor=(90, 90, 150),
                                                                   promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                            try:
                                line_end_num = int(line_end)
                            except TypeError:
                                # app = QApplication(sys.argv)
                                if line_end is not None:
                                    message_window.error('bad inputs for int ' + str(line_end))
                                return
                            try:
                                data_y = []
                                num = 0
                                avail_num = 0
                                data_y = file_data[line_num]
                                data_y = data_y[line_start_num:line_end_num + 1]
                                for i in data_y:
                                    if type(i) not in [int, float]:
                                        pass
                                    else:
                                        avail_num += 1
                                    num += 1
                                if avail_num != num and avail_num > 0:
                                    message_window.warning('we found ' + str(
                                        num - avail_num) + ' valid data in your file,we will ignore them')
                                elif avail_num == 0:
                                    message_window.error(
                                        "this program will exit because of no available value can be used to chart")
                                    return
                            except IndexError as e:
                                message_window.error(str(e))
                                return
                            if mult:
                                charts(window, clock, a, x=data, y=data_y)
                            else:
                                xs.append(data)
                                ys.append(data_y)

            if mult:# multiple separate charting windows
                if not pie:
                    charts(window, clock, chart_choices, xs=xs, ys=ys, one_table=False)
                else:
                    charts(window, clock, chart_choices, xs=xs, ys=ys, labels=pie_labels, one_table=False)

            else:# all be drawn in one window
                if not pie:
                    charts(window, clock, chart_choices, xs=xs, ys=ys, one_table=True)
                else:
                    charts(window, clock, chart_choices, xs=xs, ys=ys, labels=pie_labels, one_table=True)

            return
        except Exception as e:
            error_log = open("error_log.txt", "w")
            error_log.write("An error occurred: {}\n".format(e))
            traceback.print_exc(file=error_log)
            error_log.write("\n")
            error_log.close()
            message_window.error("An error occurred. Please check the error log for details.")
            if debug:
                raise e
            return

    else:##################################################### input manually ###############################################################################

        if mult:
            xs = ys = []
            pie = False
            pie_label = ''
        data = pyghelpers.textAnswerDialog(window, (200, 100, 500, 200),
                                           "input you data split each other with ';',(if the data isn't in a tuple or list)",
                                           'OK', 'CANCEL', backgroundColor=(90, 90, 150), promptTextColor=(0, 0, 0),
                                           inputTextColor=(0, 0, 0))
        try:
            data = data.split(";")
            data2 = []
            for i in data:
                if ('(' in i and ")" in i) or ('[' in i and "]" in i):
                    data2.append(eval(i))
                else:
                    data2.append(float(i))
            data = data2
            a = CheckBox(9, ['pie', 'hist', 'box', 'violin', 'error bar', 'hist2d', 'hexbin', 'plot', 'scatter'], 9,
                         window, clock, first_x=40, first_y=100, each_add_x=0, each_add_y=30)
            choices = a.clicked_choices
            pie_labels = []
            pie_value_poses = []
            chart_choices = []
            for a in a.clicked_choices:
                num = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200), 'How many ' +
                                                  ['pie', 'hist', 'box', 'violin', 'error bar', 'hist2d', 'hexbin',
                                                   'plot', 'scatter'][a] + ' charts do you want to draw?',
                                                  'OK',
                                                  'CANCEL', backgroundColor=(90, 90, 150),
                                                  promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                try:
                    num = int(num)
                except Exception:
                    message_window.error("Can't turn " + str(num) + ' into an integer')
                    return
                if num < 0:
                    message_window.error("You can't draw negative charts!")
                    return
                else:
                    for i in range(num):
                        chart_choices.append(a)
            for a in chart_choices:
                if type(a) is str:
                    break
                if a <= 4:
                    if a == 0:
                        label_choice = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                                  'please input the labels ', "manually",
                                                                  'automatically create')
                        if label_choice:
                            label = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                                "input you labels split each other with ';',(number:" + str(
                                                                    len(data)) + '),input none to set labels automatically',
                                                                'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                                promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                            if label is not None:
                                label = label.split(";")
                                if len(label) > len(data):
                                    message_window.warning(
                                        "label's num (" + str(len(label)) + ", is higher than data's num (" + str(
                                            len(data))
                                        + ",system will adjust this by canceling labels automatically")
                                    label = label[:len(data)]
                                elif len(label) < len(data):
                                    message_window.warning(
                                        "label's num (" + str(len(label)) + ", is lower than data's num (" + str(
                                            len(data)) + ',system will adjust this by adding labels automatically')
                                    k = len(label)
                                    label = label + ['label ' + str(k + a) for a in range(len(data) - len(label))]

                            else:
                                label = ["label " + str(b + 1) for b in range(len(data))]
                            if mult:
                                charts(window, clock, a, x=data, labels=label)
                            else:
                                pie = True
                                pie_label = label
                                pie_value_poses.append(len(xs))
                                xs.append(data)
                                pie_labels.append(pie_label)
                        else:
                            label_source = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300),
                                                                      "please select the labels' source",
                                                                      "Excel files(*.xlsx)", 'automatically create')
                            if label_source:
                                label = load_label(window, len(data))
                                if label is None:
                                    message_window.error("FATAL ERROR:failed to load labels;function ends")
                                    return
                            else:
                                label = ["label " + str(b + 1) for b in range(len(data))]
                                if mult:
                                    charts(window, clock, a, x=data, labels=label)
                                else:
                                    xs.append(data)
                            pie_label = label
                            pie_value_poses.append(len(xs))
                            xs.append(data)
                            pie_labels.append(pie_label)
                    else:
                        if mult:
                            charts(window, clock, a, x=data)
                        else:
                            xs.append(data)
                else:
                    data2 = pyghelpers.textAnswerDialog(window, (0, 0, 1004, 200),
                                                        "input you NEXT group of data ,split each other with ' ',(if the data isn't in a tuple or list)",
                                                        'OK', 'CANCEL', backgroundColor=(90, 90, 150),
                                                        promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
                    data2 = data2.split(" ")
                    if not mult:
                        charts(window, clock, a, x=data, y=data2)
                    else:
                        xs.append(data)
                        ys.append(data2)
            if mult:
                if not pie:
                    charts(window, clock, chart_choices, xs=xs, ys=ys)
                else:
                    charts(window, clock, chart_choices, xs=xs, ys=ys, labels=pie_label)
            return
        except TypeError:
            message_window.error("bad inputs for float!")
            return
        except Exception as e:
            error_log = open("error_log.txt", "w")
            error_log.write("An error occurred: {}\n".format(e))
            error_log.write("Traceback:\n")
            traceback.print_exc(file=error_log)
            error_log.write("\n")
            error_log.close()
            message_window.error("An error occurred. Please check the error log for details.")
            if debug:
                raise e
            return


def data_analyze(window):
    global message_window
    data_collecting_method = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300), 'how do you want to collect data',
                                                        '.xlsx file', "by inputting the data manually")
    analyse_choice = CheckBox(9, ['pie', 'hist', 'box', 'violin', 'error bar', 'hist2d', 'hexbin', 'plot', 'scatter'], 9,
                 window, clock, first_x=40, first_y=100, each_add_x=0, each_add_y=30)

    if data_collecting_method:#from excel files
        message_window.browser("Choose an Excel file for the data's source", [('EXCEL files', '.xlsx')])
        file_name = message_window.file_name
        if file_name == '':
            message_window.error('Failed to continue because of empty filename was given')
            return
        try:
            file = ExcelMgr(file_name)
        except Exception as e:
            message_window.error(str(e))
            return
        file_data = file.data
        list_preview = WindowListViewer(file_data, (1004, 410), window, (0, 200))
        choice = pyghelpers.textYesNoDialog(window, (0, 300, 400, 300), 'how do you want to collect data',
                                            "by line(----)", 'by column(| | |)')

        if not choice:  ####by column ################################################################################

            arrange = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200), 'input arrange number',
                                                           [list_preview.draw], [list_preview.handle_event], 'OK',
                                                           'CANCEL', backgroundColor=(90, 90, 150),
                                                           promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            try:
                arrange_num = int(arrange)
            except TypeError:
                if arrange is not None:
                    message_window.error('bad inputs for int ' + str(arrange))
                return
            cols_start = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                              'input cols start position of arrange (starts with 0)' + str(
                                                                  arrange_num), [list_preview.draw],
                                                              [list_preview.handle_event], 'OK',
                                                              'CANCEL', backgroundColor=(90, 90, 150),
                                                              promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            try:
                col_start_num = int(cols_start)
            except TypeError:
                if cols_start is not None:
                    message_window.error('bad inputs for int ' + str(cols_start))
                return
            cols_end = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                            'input cols end position of arrange (include)' + str(
                                                                arrange_num),
                                                            [list_preview.draw], [list_preview.handle_event], 'OK',
                                                            'CANCEL', backgroundColor=(90, 90, 150),
                                                            promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            try:
                col_end_num = int(cols_end)
            except TypeError:
                if cols_end is not None:
                    message_window.error('bad inputs for int ' + str(cols_end))
                return
            try:
                data = []
                num = 0
                avail_num = 0
                for i in file_data[col_start_num - 1:col_end_num]:
                    if type(i[arrange_num - 1]) in [int, float]:
                        avail_num += 1
                        data.append(i[arrange_num - 1])
                    num += 1
                if avail_num != num:
                    message_window.warning('we found ' + str(
                        num - avail_num) + ' valid data(s) in your file,we will ignore them(it)')
                if len(data) == 0:
                    message_window.error('Exit because of no available data')
                    return
            except IndexError as e:
                message_window.error(str(e))
                return

        else: ##### by line ################################################################################

            line = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200), 'input line number', [list_preview.draw]
                                                    , [list_preview.handle_event], 'OK',
                                                    'CANCEL', backgroundColor=(90, 90, 150),
                                                    promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            try:
                line_num = int(line)
            except TypeError:
                if line is not None:
                    message_window.error('bad inputs for int ' + str(line))
                return
            line_start = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                          'input arrange start position("0"means arrange 1) of line ' + str(
                                                              line_num), [list_preview.draw],
                                                          [list_preview.handle_event], 'OK', 'CANCEL',
                                                          backgroundColor=(90, 90, 150),
                                                          promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            try:
                line_start_num = int(line_start)
            except TypeError:
                if line_start is not None:
                    message_window.error('bad inputs for int ' + str(line_start))
                return
            line_end = textAnswerDialogEventProgressing(window, (0, 0, 1004, 200),
                                                        'input arrange end position of line ' + str(line_num),
                                                        [list_preview.draw], [list_preview.handle_event], 'OK',
                                                        'CANCEL', backgroundColor=(90, 90, 150),
                                                        promptTextColor=(0, 0, 0), inputTextColor=(0, 0, 0))
            try:
                line_end_num = int(line_end)
            except TypeError:
                if line_end is not None:
                    message_window.error('bad inputs for int ' + str(line_end))
                return
            try:
                num = 0
                avail_num = 0
                data = file_data[line_num]
                data = data[line_start_num:line_end_num + 1]
                for i in data:
                    if type(i) not in [int, float]:
                        pass
                    else:
                        avail_num += 1
                    num += 1
                if avail_num != num:
                    message_window.warning('we found ' + str(
                        num - avail_num) + ' valid data in your file,we will ignore them')
                if len(data) == 0:
                    return
            except IndexError as e:
                message_window.error(str(e))
                return



if __name__ == '__main__':
    window = pygame.display.set_mode((1004, 600))
    clock = pygame.time.Clock()
    data_charter(window, clock, debug=True)
    pygame.quit()
    sys.exit(0)
