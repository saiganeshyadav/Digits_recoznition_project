from kivy.app import App
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.uix.widget import Widget
from kivy.graphics import Line
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.config import Config


import PIL.Image as pilm
import numpy as np
import matplotlib.pyplot as plt


import sklearn
from sklearn.externals import joblib
from kivy.core.window import Window


#Config.set('graphics','width','960')
#Config.set('graphics','height','540')


class Touch_widget(Widget):

    line_width = 6
    l = []
    r = 0
    stops = []
    initial = 0
    d = dict()
    character = ''


    #values = {0 : 48,1 : 49,2 : 50,3 : 51,4 : 52,5 : 53,6 : 54,7 : 55,8 : 56,9 : 57,10 : 65,11 : 66,12 : 67,13 : 68,14 : 69,15 : 70,16 : 71,17 : 72,18 : 73,19 : 74,20 : 75,21 : 76,22 : 77,23 : 78,24 : 79,25 : 80,26 : 81,27 : 82,28 : 83,29 : 84,30 : 85,31 : 86,32 : 87,33 : 88,34 : 89,35 : 90,36 : 97,37 : 98,38 : 100,39 : 101,40 : 102,41 : 103,42 : 104,43 : 110,44 : 113,45 : 114,46 : 116}


    def on_touch_down(self, touch):

        if Widget.on_touch_up(self,touch):
            print('hii')
        else:
            with self.canvas:
                touch.ud['line'] = Line(points = (touch.x,touch.y),width = self.line_width)

    def on_touch_move(self, touch):
        touch.ud['line'].points += (touch.x, touch.y)

    def on_touch_up(self, touch):

        if Widget.on_touch_down(self, touch):
            print('hii')

        else:
                size = Window.size
                #print(size[0])

                x_mul = 100 / size[0]
                y_mul = 100 / size[1]

                #print(x_mul)
                #print(y_mul)

                self.r = self.r + 1


                for i in touch.ud['line'].points:
                    if touch.ud['line'].points.index(i) % 2 == 0:
                        self.l.append(i * x_mul)
                    else:
                        self.l.append(i * y_mul)

                #print(self.l)

                s = len(self.l)
                self.stops.append(s)








    def export(self):

        for k in self.stops:
            self.d[k] = self.l[self.initial : k]
            self.initial = k

        #print(list(self.d.values()))

        self.my_image = Image(source='black_bg1.jpg')
        with self.my_image.canvas:
            for l in list(self.d.values()):

                self.line = Line(points=(l), width=5)
                #Color(1, 0, 0, 0.5, mode="rgba")

        Clock.schedule_once(self.exp, 1)




        #self.my_image.export_as_image().save('cool3.jpg')








    def clear(self):
        saved = self.children[:]
        self.clear_widgets()
        self.canvas.clear()
        for widget in saved:
            self.add_widget(widget)


        self.l = []
        self.r = 0
        self.initial = 0
        self.stops = []
        self.d = dict()
        self.character = ''
        my_label = self.ids.my_label

        my_label.text = ''



    def exp(self,dd):

        self.my_image.export_as_image().save('predictedimg.jpg')

        org = pilm.open('predictedimg.jpg').convert('L')
        resized_img = org.resize((28, 28))

        resized_arr = np.asarray(resized_img)

        plt.imshow(resized_arr)

        mlp = joblib.load('mlp_digits_model')

        #print(mlp.predict(resized_arr.reshape(1, 784)))

        val = mlp.predict(resized_arr.reshape(1, 784))

        print(val)

        num = val[0]

        print(str(num))

        self.character = self.character + str(num)
        #print(self.character)

        my_label = self.ids.my_label

        my_label.text = self.character

        #size = Window.size
        #print(size)
        plt.show()








class Digit_recoznitionApp(App):
    def build(self):
        return Touch_widget()

touching = Digit_recoznitionApp()
touching.run()