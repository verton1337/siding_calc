from kivy.app import App 
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.textinput import TextInput 


from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')


import re



class FloatInput(TextInput):

    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)
"""    def on_focus(self, instance, touch):
	        self.text = ""
	        #return super(FloatInput, self).on_focus()"""	

class SidingCalcApp(App):

	def show_result(self, instance):
		first_floor = (float(self.w_f_flour.text) + float(self.ww_f_flour.text))*2*float(self.h_f_flour.text)
		result = {}
		second_floor = float(self.w_s_flour.text)*float(self.h_s_flour.text)
		winds = 0 
		result['okonn_result'] = 0
		for i in range(len(self.winds_array)):
			winds += float(self.winds_array[i][0].text) * float(self.winds_array[i][1].text)
			result['okonn_result']+= round((float(self.winds_array[i][0].text)+ 2 * float(self.winds_array[i][1].text))/float(self.planky.text)) 
		result['okonn_result'] = round(result['okonn_result']*1.05)+1
		#result['siding_result'] = round((first_floor + second_floor - winds)/(float(self.siding_w.text)*float(self.siding_h.text)) * 1.05)
		#result['siding_result'] = round((( + second_floor/(float(self.siding_w.text)*float(self.siding_h.text))) * 1.05)
		result['siding_result'] = (float(self.w_f_flour.text) + float(self.ww_f_flour.text))*2 #Poluchili perimetr

		result['siding_result'] = result['siding_result']//float(self.siding_w.text)+1 #Poluchili kolichestvo paneley po perimetru

		result['siding_result'] = result['siding_result']*((float(self.h_f_flour.text)//float(self.siding_h.text))) # Poluchili kol-vo paneley na 1 etazh

		result['siding_result'] = round(result['siding_result'] + 2*second_floor/((float(self.siding_w.text)*float(self.siding_h.text))))

		result['start_result'] = round(2* (float(self.w_f_flour.text) + float(self.ww_f_flour.text))/float(self.planky.text))
		
		result['jtrim_result'] = 1 + round((2 * (float(self.w_f_flour.text) + float(self.ww_f_flour.text) - float(self.w_s_flour.text)) + (float(self.h_s_flour.text)**2+float(self.w_s_flour.text)**2)**(.5)*4)/float(self.planky.text))
		if float(self.h_f_flour.text) > float(self.planky.text):
			if float(self.h_f_flour.text) / float(self.planky.text) > 0.5:
				result['nar_ug_result'] = 8
			else: result['nar_ug_result'] = 6
		else: result['nar_ug_result'] = 4
		result['soed_result'] = (float(self.w_f_flour.text) // float(self.siding_w.text) + float(self.h_f_flour.text) // float(self.siding_w.text) + float(self.w_s_flour.text) // float(self.siding_w.text)) * 2
		print(result)
		self.footerlayout.remove_widget(self.windows_footerlayout)
		self.footerlayout.add_widget(Label(text = 'Необходимые комплектующие:'))
		result_layout = GridLayout(cols = 2)

		result_layout.add_widget(Label(text = 'Панелей - '))
		result_layout.add_widget(Label(text = str(result['siding_result'])))

		result_layout.add_widget(Label(text = 'Стартовых - '))
		result_layout.add_widget(Label(text = str(result['start_result'])))

		result_layout.add_widget(Label(text = 'J-профилей - '))
		result_layout.add_widget(Label(text = str(result['jtrim_result'])))

		result_layout.add_widget(Label(text = 'Околооконок - '))
		result_layout.add_widget(Label(text = str(result['okonn_result'])))

		result_layout.add_widget(Label(text = 'Наружних углов - '))
		result_layout.add_widget(Label(text = str(result['nar_ug_result'])))

		result_layout.add_widget(Label(text = 'Соединителей - '))
		result_layout.add_widget(Label(text = str(result['soed_result'])))
		self.footerlayout.add_widget(result_layout)

	def add_windows(self, instance):
		wind_inputs = []
		for i in range(int(self.window_col.text)):
			wind = GridLayout(cols = 3)

			wind.add_widget(Label(text = "Ширина"))
			wind.add_widget(Widget())
			wind.add_widget(Label(text = "Высота"))
			wind_inputs.append(FloatInput())
			wind.add_widget(wind_inputs[len(wind_inputs)-1])

			wind.add_widget(Label(text = "X"))
			wind.add_widget(FloatInput())
			

			self.windows_footerlayout.add_widget(wind)
			self.winds_array.append(wind_inputs)

		self.footerlayout.remove_widget(self.hintlayout)
		self.footerlayout.add_widget(self.windows_footerlayout)

		self.footerlayout.add_widget(Button(text = "Рассчитать" , size_hint = (.3,.15), pos_hint = {'left':0}, on_press = self.show_result))
	
	def build(self):
		self.winds_array = []
		mainlayout = BoxLayout(orientation = "vertical")

		headerlayout = BoxLayout(orientation = "vertical", size_hint = (1,.2))
		headerlayout.add_widget(Label(text = 'Размеры планок'))

		self.siding_w = FloatInput(text = 'Длина сайдинга')
		self.siding_h = FloatInput(text = 'Высота сайдинга')
		self.planky = FloatInput(text = 'Длина планок')
		siding_layout = BoxLayout()
		siding_layout.add_widget(self.siding_w)
		siding_layout.add_widget(self.siding_h)
		siding_layout.add_widget(self.planky)
		headerlayout.add_widget(siding_layout)

		left_centerlayout = GridLayout(cols = 2)
		left_centerlayout.add_widget(Label(text = "1 этаж"))
		left_centerlayout.add_widget(Widget())
		
		left_centerlayout.add_widget(Label(text = "Длина"))
		self.w_f_flour = FloatInput()
		left_centerlayout.add_widget(self.w_f_flour)
		

		left_centerlayout.add_widget(Label(text = "Ширина"))
		self.ww_f_flour = FloatInput()
		left_centerlayout.add_widget(self.ww_f_flour)

		left_centerlayout.add_widget(Label(text = "Высота"))
		self.h_f_flour = FloatInput()
		left_centerlayout.add_widget(self.h_f_flour)


		right_centerlayout = GridLayout(cols = 2)
		right_centerlayout.add_widget(Label(text = "2 этаж (Фронтон)"))
		right_centerlayout.add_widget(Widget())

		right_centerlayout.add_widget(Label(text = "Ширина"))
		self.w_s_flour = FloatInput()
		right_centerlayout.add_widget(self.w_s_flour)

		right_centerlayout.add_widget(Label(text = "Высота"))
		self.h_s_flour = FloatInput()
		right_centerlayout.add_widget(self.h_s_flour)


		centerlayout = BoxLayout(orientation = "horizontal", padding = 30, size_hint = (1,.5))
		centerlayout.add_widget(left_centerlayout)
		centerlayout.add_widget(right_centerlayout)

		self.footerlayout = BoxLayout(orientation = "vertical")

		self.hintlayout = BoxLayout(orientation = "horizontal", spacing = 3, padding = 30)
		self.hintlayout.add_widget(Label(text = "Окна/двери: ", size_hint = (1,.15), pos_hint = {'top':1}))
		self.window_col = FloatInput(size_hint = (1,.15), pos_hint = {'top':1})
		self.hintlayout.add_widget(self.window_col)
		self.hintlayout.add_widget(Button(text = "Добавить", size_hint = (1,.15), pos_hint = {'top':1}, on_press = self.add_windows))

		self.footerlayout.add_widget(self.hintlayout)
		self.windows_footerlayout = GridLayout(cols = 3)

		mainlayout.add_widget(headerlayout)
		mainlayout.add_widget(centerlayout)
		mainlayout.add_widget(self.footerlayout)

		return mainlayout





if __name__ == "__main__":
	SidingCalcApp().run()