from odoo import models, fields, api
from datetime import date

class EmployeeMaster(models.Model):
    _name = 'employee.master'
    _description = 'Employee Master'

    name = fields.Char("Name")
    age = fields.Integer("Age")
    date_of_birth = fields.Date("Date of Birth")
    location = fields.Char("Location")

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")

    image = fields.Binary("Image")

    salary = fields.Float("Salary")
    employee_tax = fields.Float("Employee Tax")
    employee_pf = fields.Float("Employee PF")
    net_salary = fields.Float("Net Salary")

    is_resident_mumbai = fields.Boolean("Is Resident of Mumbai")

    @api.onchange('date_of_birth')
    def calculate_age(self):
        if self.date_of_birth:
            today = date.today()
            self.age = today.year - self.date_of_birth.year

    @api.onchange('salary','age','gender','is_resident_mumbai')
    def calculate_net_salary(self):
        if self.salary:
            net = self.salary


            if self.is_resident_mumbai:
                net = net - (self.salary * 0.10)
            else:
                net = net + (self.salary * 0.10)


            if self.age > 25:
                net = net - self.employee_tax


            if self.gender == 'male':
                self.employee_pf = self.salary * 0.05
                net = net - self.employee_pf
            elif self.gender == 'female':
                self.employee_pf = self.salary * 0.03
                net = net - self.employee_pf
            elif self.gender == 'other':
                net = net + (self.salary * 0.05)

            self.net_salary = net