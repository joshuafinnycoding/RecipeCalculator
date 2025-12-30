from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, NumericProperty
import json
import os


# Data Models
class Ingredient:
    def __init__(self, name, quantity, unit, cost):
        self.name = name
        self.quantity = float(quantity)
        self.unit = unit
        self.cost = float(cost)
    
    def to_dict(self):
        return {
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit,
            'cost': self.cost
        }
    
    @staticmethod
    def from_dict(data):
        return Ingredient(data['name'], data['quantity'], data['unit'], data['cost'])


class Product:
    def __init__(self, name, quantity, unit, ingredients=None):
        self.name = name
        self.quantity = float(quantity)
        self.unit = unit
        self.ingredients = ingredients if ingredients else []
    
    def add_ingredient(self, ingredient_name, quantity, unit):
        self.ingredients.append({
            'name': ingredient_name,
            'quantity': float(quantity),
            'unit': unit
        })
    
    def to_dict(self):
        return {
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit,
            'ingredients': self.ingredients
        }
    
    @staticmethod
    def from_dict(data):
        return Product(
            data['name'],
            data['quantity'],
            data['unit'],
            data.get('ingredients', [])
        )


# Data Manager
class DataManager:
    def __init__(self):
        self.ingredients_file = 'ingredients.json'
        self.products_file = 'products.json'
        self.ingredients = {}
        self.products = {}
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.ingredients_file):
            with open(self.ingredients_file, 'r') as f:
                data = json.load(f)
                self.ingredients = {k: Ingredient.from_dict(v) for k, v in data.items()}
        
        if os.path.exists(self.products_file):
            with open(self.products_file, 'r') as f:
                data = json.load(f)
                self.products = {k: Product.from_dict(v) for k, v in data.items()}
    
    def save_data(self):
        with open(self.ingredients_file, 'w') as f:
            json.dump({k: v.to_dict() for k, v in self.ingredients.items()}, f)
        
        with open(self.products_file, 'w') as f:
            json.dump({k: v.to_dict() for k, v in self.products.items()}, f)
    
    def add_ingredient(self, ingredient):
        self.ingredients[ingredient.name] = ingredient
        self.save_data()
    
    def add_product(self, product):
        self.products[product.name] = product
        self.save_data()
    
    def get_ingredient(self, name):
        return self.ingredients.get(name)
    
    def get_product(self, name):
        return self.products.get(name)
    
    def update_ingredient_cost(self, name, new_cost):
        if name in self.ingredients:
            self.ingredients[name].cost = float(new_cost)
            self.save_data()


# Screens
class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(text='Recipe Calculator', font_size='24sp', size_hint_y=0.2)
        layout.add_widget(title)
        
        btn_add_ingredient = Button(text='Add Ingredients', size_hint_y=0.15)
        btn_add_ingredient.bind(on_press=lambda x: setattr(self.manager, 'current', 'add_ingredient'))
        layout.add_widget(btn_add_ingredient)
        
        btn_add_product = Button(text='Add Products', size_hint_y=0.15)
        btn_add_product.bind(on_press=lambda x: setattr(self.manager, 'current', 'add_product'))
        layout.add_widget(btn_add_product)
        
        btn_scale = Button(text='Scale Recipe', size_hint_y=0.15)
        btn_scale.bind(on_press=lambda x: setattr(self.manager, 'current', 'scale_recipe'))
        layout.add_widget(btn_scale)
        
        btn_pricing = Button(text='Pricing', size_hint_y=0.15)
        btn_pricing.bind(on_press=lambda x: setattr(self.manager, 'current', 'pricing'))
        layout.add_widget(btn_pricing)
        
        btn_manage = Button(text='Manage Ingredients', size_hint_y=0.15)
        btn_manage.bind(on_press=lambda x: setattr(self.manager, 'current', 'manage_ingredients'))
        layout.add_widget(btn_manage)
        
        self.add_widget(layout)


class AddIngredientScreen(Screen):
    def __init__(self, data_manager, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = data_manager
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(text='Add Ingredient', font_size='20sp', size_hint_y=0.1)
        layout.add_widget(title)
        
        # Input fields
        form = GridLayout(cols=2, spacing=10, size_hint_y=0.6)
        
        form.add_widget(Label(text='Name:'))
        self.name_input = TextInput(multiline=False)
        form.add_widget(self.name_input)
        
        form.add_widget(Label(text='Quantity:'))
        self.quantity_input = TextInput(multiline=False, input_filter='float')
        form.add_widget(self.quantity_input)
        
        form.add_widget(Label(text='Unit:'))
        self.unit_spinner = Spinner(text='grams', values=['grams', 'milliliters', 'pieces'])
        form.add_widget(self.unit_spinner)
        
        form.add_widget(Label(text='Cost (INR):'))
        self.cost_input = TextInput(multiline=False, input_filter='float')
        form.add_widget(self.cost_input)
        
        layout.add_widget(form)
        
        # Buttons
        btn_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        
        btn_save = Button(text='Save Ingredient')
        btn_save.bind(on_press=self.save_ingredient)
        btn_layout.add_widget(btn_save)
        
        btn_back = Button(text='Back')
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main_menu'))
        btn_layout.add_widget(btn_back)
        
        layout.add_widget(btn_layout)
        self.add_widget(layout)
    
    def save_ingredient(self, instance):
        try:
            name = self.name_input.text.strip()
            quantity = float(self.quantity_input.text)
            unit = self.unit_spinner.text
            cost = float(self.cost_input.text)
            
            if not name:
                self.show_popup('Error', 'Please enter ingredient name')
                return
            
            ingredient = Ingredient(name, quantity, unit, cost)
            self.data_manager.add_ingredient(ingredient)
            
            self.show_popup('Success', f'Ingredient "{name}" added successfully!')
            self.clear_inputs()
        except ValueError:
            self.show_popup('Error', 'Please enter valid numbers for quantity and cost')
    
    def clear_inputs(self):
        self.name_input.text = ''
        self.quantity_input.text = ''
        self.cost_input.text = ''
    
    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.3))
        popup.open()


class ManageIngredientsScreen(Screen):
    def __init__(self, data_manager, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = data_manager
        
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(text='Manage Ingredients', font_size='20sp', size_hint_y=0.1)
        self.layout.add_widget(title)
        
        self.scroll_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.scroll_layout.bind(minimum_height=self.scroll_layout.setter('height'))
        
        scroll = ScrollView(size_hint_y=0.7)
        scroll.add_widget(self.scroll_layout)
        self.layout.add_widget(scroll)
        
        btn_back = Button(text='Back', size_hint_y=0.1)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main_menu'))
        self.layout.add_widget(btn_back)
        
        self.add_widget(self.layout)
    
    def on_enter(self):
        self.refresh_list()
    
    def refresh_list(self):
        self.scroll_layout.clear_widgets()
        
        for name, ingredient in self.data_manager.ingredients.items():
            item_layout = BoxLayout(size_hint_y=None, height=60, spacing=5)
            
            info = f"{name}\n{ingredient.quantity} {ingredient.unit} - ₹{ingredient.cost}"
            item_layout.add_widget(Label(text=info, size_hint_x=0.6))
            
            btn_edit = Button(text='Edit Cost', size_hint_x=0.4)
            btn_edit.bind(on_press=lambda x, n=name: self.edit_cost(n))
            item_layout.add_widget(btn_edit)
            
            self.scroll_layout.add_widget(item_layout)
    
    def edit_cost(self, ingredient_name):
        ingredient = self.data_manager.get_ingredient(ingredient_name)
        
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=f'Edit cost for {ingredient_name}'))
        
        cost_input = TextInput(text=str(ingredient.cost), multiline=False, input_filter='float')
        content.add_widget(cost_input)
        
        btn_layout = BoxLayout(spacing=10)
        
        popup = Popup(title='Edit Cost', content=content, size_hint=(0.8, 0.4))
        
        btn_save = Button(text='Save')
        btn_save.bind(on_press=lambda x: self.save_cost(ingredient_name, cost_input.text, popup))
        btn_layout.add_widget(btn_save)
        
        btn_cancel = Button(text='Cancel')
        btn_cancel.bind(on_press=popup.dismiss)
        btn_layout.add_widget(btn_cancel)
        
        content.add_widget(btn_layout)
        popup.open()
    
    def save_cost(self, ingredient_name, new_cost, popup):
        try:
            self.data_manager.update_ingredient_cost(ingredient_name, new_cost)
            popup.dismiss()
            self.refresh_list()
        except ValueError:
            pass


class AddProductScreen(Screen):
    def __init__(self, data_manager, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = data_manager
        self.product_ingredients = []
        
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(text='Add Product', font_size='20sp', size_hint_y=0.08)
        self.layout.add_widget(title)
        
        # Product info
        product_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.15)
        product_layout.add_widget(Label(text='Product Name:'))
        self.product_name = TextInput(multiline=False)
        product_layout.add_widget(self.product_name)
        
        product_layout.add_widget(Label(text='Quantity:'))
        self.product_quantity = TextInput(multiline=False, input_filter='float')
        product_layout.add_widget(self.product_quantity)
        
        product_layout.add_widget(Label(text='Unit:'))
        self.product_unit = Spinner(text='grams', values=['grams', 'milliliters', 'pieces'])
        product_layout.add_widget(self.product_unit)
        
        self.layout.add_widget(product_layout)
        
        # Add ingredient section
        ing_title = Label(text='Add Ingredients', size_hint_y=0.05)
        self.layout.add_widget(ing_title)
        
        ing_form = GridLayout(cols=2, spacing=10, size_hint_y=0.15)
        
        ing_form.add_widget(Label(text='Ingredient:'))
        self.ing_spinner = Spinner(text='Select', values=['Select'])
        ing_form.add_widget(self.ing_spinner)
        
        ing_form.add_widget(Label(text='Quantity:'))
        self.ing_quantity = TextInput(multiline=False, input_filter='float')
        ing_form.add_widget(self.ing_quantity)
        
        ing_form.add_widget(Label(text='Unit:'))
        self.ing_unit = Spinner(text='grams', values=['grams', 'milliliters', 'pieces'])
        ing_form.add_widget(self.ing_unit)
        
        self.layout.add_widget(ing_form)
        
        btn_add_ing = Button(text='Add Ingredient to Product', size_hint_y=0.08)
        btn_add_ing.bind(on_press=self.add_ingredient_to_product)
        self.layout.add_widget(btn_add_ing)
        
        # List of added ingredients
        self.ing_list_label = Label(text='Ingredients: None added yet', size_hint_y=0.2)
        self.layout.add_widget(self.ing_list_label)
        
        # Buttons
        btn_layout = BoxLayout(size_hint_y=0.15, spacing=10)
        
        btn_save = Button(text='Save Product')
        btn_save.bind(on_press=self.save_product)
        btn_layout.add_widget(btn_save)
        
        btn_back = Button(text='Back')
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main_menu'))
        btn_layout.add_widget(btn_back)
        
        self.layout.add_widget(btn_layout)
        self.add_widget(self.layout)
    
    def on_enter(self):
        ingredients = list(self.data_manager.ingredients.keys())
        if ingredients:
            self.ing_spinner.values = ingredients
            self.ing_spinner.text = ingredients[0]
        else:
            self.ing_spinner.values = ['No ingredients available']
            self.ing_spinner.text = 'No ingredients available'
    
    def add_ingredient_to_product(self, instance):
        try:
            ing_name = self.ing_spinner.text
            if ing_name == 'Select' or ing_name == 'No ingredients available':
                self.show_popup('Error', 'Please select an ingredient')
                return
            
            quantity = float(self.ing_quantity.text)
            unit = self.ing_unit.text
            
            self.product_ingredients.append({
                'name': ing_name,
                'quantity': quantity,
                'unit': unit
            })
            
            self.update_ingredient_list()
            self.ing_quantity.text = ''
        except ValueError:
            self.show_popup('Error', 'Please enter valid quantity')
    
    def update_ingredient_list(self):
        if self.product_ingredients:
            text = 'Ingredients:\n'
            for ing in self.product_ingredients:
                text += f"- {ing['name']}: {ing['quantity']} {ing['unit']}\n"
            self.ing_list_label.text = text
        else:
            self.ing_list_label.text = 'Ingredients: None added yet'
    
    def save_product(self, instance):
        try:
            name = self.product_name.text.strip()
            quantity = float(self.product_quantity.text)
            unit = self.product_unit.text
            
            if not name:
                self.show_popup('Error', 'Please enter product name')
                return
            
            if not self.product_ingredients:
                self.show_popup('Error', 'Please add at least one ingredient')
                return
            
            product = Product(name, quantity, unit, self.product_ingredients.copy())
            self.data_manager.add_product(product)
            
            self.show_popup('Success', f'Product "{name}" added successfully!')
            self.clear_inputs()
        except ValueError:
            self.show_popup('Error', 'Please enter valid numbers')
    
    def clear_inputs(self):
        self.product_name.text = ''
        self.product_quantity.text = ''
        self.product_ingredients = []
        self.update_ingredient_list()
        self.ing_quantity.text = ''
    
    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.3))
        popup.open()


class ScaleRecipeScreen(Screen):
    def __init__(self, data_manager, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = data_manager
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(text='Scale Recipe', font_size='20sp', size_hint_y=0.1)
        layout.add_widget(title)
        
        form = GridLayout(cols=2, spacing=10, size_hint_y=0.25)
        
        form.add_widget(Label(text='Select Product:'))
        self.product_spinner = Spinner(text='Select', values=['Select'])
        form.add_widget(self.product_spinner)
        
        form.add_widget(Label(text='New Quantity:'))
        self.new_quantity = TextInput(multiline=False, input_filter='float')
        form.add_widget(self.new_quantity)
        
        form.add_widget(Label(text='Unit:'))
        self.new_unit = Spinner(text='grams', values=['grams', 'milliliters', 'pieces'])
        form.add_widget(self.new_unit)
        
        layout.add_widget(form)
        
        btn_scale = Button(text='Scale Recipe', size_hint_y=0.1)
        btn_scale.bind(on_press=self.scale_recipe)
        layout.add_widget(btn_scale)
        
        self.result_label = Label(text='', size_hint_y=0.3)
        layout.add_widget(self.result_label)
        
        save_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.1)
        save_layout.add_widget(Label(text='Save as:'))
        self.new_product_name = TextInput(multiline=False)
        save_layout.add_widget(self.new_product_name)
        layout.add_widget(save_layout)
        
        btn_layout = BoxLayout(size_hint_y=0.15, spacing=10)
        
        btn_save = Button(text='Save New Product')
        btn_save.bind(on_press=self.save_scaled_product)
        btn_layout.add_widget(btn_save)
        
        btn_back = Button(text='Back')
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main_menu'))
        btn_layout.add_widget(btn_back)
        
        layout.add_widget(btn_layout)
        self.add_widget(layout)
        
        self.scaled_ingredients = []
    
    def on_enter(self):
        products = list(self.data_manager.products.keys())
        if products:
            self.product_spinner.values = products
            self.product_spinner.text = products[0]
        else:
            self.product_spinner.values = ['No products available']
            self.product_spinner.text = 'No products available'
    
    def scale_recipe(self, instance):
        try:
            product_name = self.product_spinner.text
            if product_name == 'Select' or product_name == 'No products available':
                self.show_popup('Error', 'Please select a product')
                return
            
            new_quantity = float(self.new_quantity.text)
            new_unit = self.new_unit.text
            
            product = self.data_manager.get_product(product_name)
            
            # Calculate scaling factor
            if product.unit != new_unit:
                self.show_popup('Warning', 'Unit mismatch! Results may be inaccurate.')
            
            scale_factor = new_quantity / product.quantity
            
            self.scaled_ingredients = []
            result_text = f'Scaled recipe for {new_quantity} {new_unit}:\n\n'
            
            for ing in product.ingredients:
                scaled_qty = ing['quantity'] * scale_factor
                self.scaled_ingredients.append({
                    'name': ing['name'],
                    'quantity': scaled_qty,
                    'unit': ing['unit']
                })
                result_text += f"{ing['name']}: {scaled_qty:.2f} {ing['unit']}\n"
            
            self.result_label.text = result_text
            self.new_product_name.text = f"{product_name}_scaled"
            
        except ValueError:
            self.show_popup('Error', 'Please enter valid quantity')
    
    def save_scaled_product(self, instance):
        try:
            if not self.scaled_ingredients:
                self.show_popup('Error', 'Please scale a recipe first')
                return
            
            name = self.new_product_name.text.strip()
            if not name:
                self.show_popup('Error', 'Please enter product name')
                return
            
            new_quantity = float(self.new_quantity.text)
            new_unit = self.new_unit.text
            
            product = Product(name, new_quantity, new_unit, self.scaled_ingredients.copy())
            self.data_manager.add_product(product)
            
            self.show_popup('Success', f'Scaled product "{name}" saved!')
            self.result_label.text = ''
            self.new_quantity.text = ''
            self.new_product_name.text = ''
            
        except ValueError:
            self.show_popup('Error', 'Invalid input')
    
    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.3))
        popup.open()


class PricingScreen(Screen):
    def __init__(self, data_manager, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = data_manager
        
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(text='Product Pricing', font_size='20sp', size_hint_y=0.08)
        main_layout.add_widget(title)
        
        scroll = ScrollView(size_hint_y=0.7)
        layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        
        layout.add_widget(Label(text='Select Product:', size_hint_y=None, height=40))
        self.product_spinner = Spinner(text='Select', values=['Select'], size_hint_y=None, height=40)
        layout.add_widget(self.product_spinner)
        
        layout.add_widget(Label(text='Wastage (%):',size_hint_y=None, height=40))
        self.wastage = TextInput(text='0', multiline=False, input_filter='float', size_hint_y=None, height=40)
        layout.add_widget(self.wastage)
        
        layout.add_widget(Label(text='Utilities (₹):', size_hint_y=None, height=40))
        self.utilities = TextInput(text='0', multiline=False, input_filter='float', size_hint_y=None, height=40)
        layout.add_widget(self.utilities)
        
        layout.add_widget(Label(text='Packaging (₹):', size_hint_y=None, height=40))
        self.packaging = TextInput(text='0', multiline=False, input_filter='float', size_hint_y=None, height=40)
        layout.add_widget(self.packaging)
        
        layout.add_widget(Label(text='Shipping (₹):', size_hint_y=None, height=40))
        self.shipping = TextInput(text='0', multiline=False, input_filter='float', size_hint_y=None, height=40)
        layout.add_widget(self.shipping)
        
        layout.add_widget(Label(text='Taxes (%):', size_hint_y=None, height=40))
        self.taxes = TextInput(text='0', multiline=False, input_filter='float', size_hint_y=None, height=40)
        layout.add_widget(self.taxes)
        
        layout.add_widget(Label(text='Labour (₹):', size_hint_y=None, height=40))
        self.labour = TextInput(text='0', multiline=False, input_filter='float', size_hint_y=None, height=40)
        layout.add_widget(self.labour)
        
        layout.add_widget(Label(text='Profit Margin (%):', size_hint_y=None, height=40))
        self.profit = TextInput(text='0', multiline=False, input_filter='float', size_hint_y=None, height=40)
        layout.add_widget(self.profit)
        
        scroll.add_widget(layout)
        main_layout.add_widget(scroll)
        
        btn_calculate = Button(text='Calculate Price', size_hint_y=0.08)
        btn_calculate.bind(on_press=self.calculate_price)
        main_layout.add_widget(btn_calculate)
        
        self.result_label = Label(text='', size_hint_y=0.12, font_size='16sp')
        main_layout.add_widget(self.result_label)
        
        btn_back = Button(text='Back', size_hint_y=0.08)
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main_menu'))
        main_layout.add_widget(btn_back)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        products = list(self.data_manager.products.keys())
        if products:
            self.product_spinner.values = products
            self.product_spinner.text = products[0]
        else:
            self.product_spinner.values = ['No products available']
            self.product_spinner.text = 'No products available'
    
    def calculate_price(self, instance):
        try:
            product_name = self.product_spinner.text
            if product_name == 'Select' or product_name == 'No products available':
                self.show_popup('Error', 'Please select a product')
                return
            
            product = self.data_manager.get_product(product_name)
            
            # Calculate base cost from ingredients
            base_cost = 0
            for ing_data in product.ingredients:
                ingredient = self.data_manager.get_ingredient(ing_data['name'])
                if ingredient:
                    # Calculate cost based on quantity
                    cost_per_unit = ingredient.cost / ingredient.quantity
                    ing_cost = cost_per_unit * ing_data['quantity']
                    base_cost += ing_cost
            
            # Apply wastage percentage
            wastage_pct = float(self.wastage.text) / 100
            wastage_cost = base_cost * wastage_pct
            
            # Apply taxes percentage
            taxes_pct = float(self.taxes.text) / 100
            taxes_cost = base_cost * taxes_pct
            
            # Add fixed costs
            utilities_cost = float(self.utilities.text)
            packaging_cost = float(self.packaging.text)
            shipping_cost = float(self.shipping.text)
            labour_cost = float(self.labour.text)
            
            # Calculate subtotal
            subtotal = (base_cost + wastage_cost + taxes_cost + 
                       utilities_cost + packaging_cost + shipping_cost + labour_cost)
            
            # Apply profit margin
            profit_pct = float(self.profit.text) / 100
            profit_amount = subtotal * profit_pct
            
            final_price = subtotal + profit_amount
            
            # Display breakdown
            result = f'Price Breakdown for {product_name}:\n'
            result += f'Base Cost: ₹{base_cost:.2f}\n'
            result += f'Wastage ({self.wastage.text}%): ₹{wastage_cost:.2f}\n'
            result += f'Utilities: ₹{utilities_cost:.2f}\n'
            result += f'Packaging: ₹{packaging_cost:.2f}\n'
            result += f'Shipping: ₹{shipping_cost:.2f}\n'
            result += f'Taxes ({self.taxes.text}%): ₹{taxes_cost:.2f}\n'
            result += f'Labour: ₹{labour_cost:.2f}\n'
            result += f'Subtotal: ₹{subtotal:.2f}\n'
            result += f'Profit ({self.profit.text}%): ₹{profit_amount:.2f}\n'
            result += f'\nFINAL PRICE: ₹{final_price:.2f}'
            
            self.result_label.text = result
            
        except ValueError as e:
            self.show_popup('Error', 'Please enter valid numbers')
    
    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.3))
        popup.open()


class RecipeCalculatorApp(App):
    def build(self):
        self.title = 'Recipe Calculator'
        self.data_manager = DataManager()
        
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(AddIngredientScreen(self.data_manager, name='add_ingredient'))
        sm.add_widget(ManageIngredientsScreen(self.data_manager, name='manage_ingredients'))
        sm.add_widget(AddProductScreen(self.data_manager, name='add_product'))
        sm.add_widget(ScaleRecipeScreen(self.data_manager, name='scale_recipe'))
        sm.add_widget(PricingScreen(self.data_manager, name='pricing'))
        
        return sm


if __name__ == '__main__':
    RecipeCalculatorApp().run()