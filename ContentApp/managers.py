from django.db import models

class PricingManager(models.Manager):
    def get_object_pricing(self,object,date,adults,children_age=None):
        pricing_objects = object.pricing_set.all()
        for obj in pricing_objects:
            if obj.valid_from_date and obj.valid_till_date and date >= obj.valid_from_date and date <= obj.valid_till_date:
                children = 0
                if children_age:
                    children_age_list = children_age.split(',')
                    for i in range(len(children_age_list)):
                        age = int(children_age_list[i])
                        if age >= obj.adult_cutoff_age:
                            adults += 1
                        elif age >= obj.child_cutoff_age:
                            children += 1
                total_pax = adults + children
                if obj.pricing_type == 'FLAT':
                    price = (adults*obj.flat_adult_price + children*obj.flat_child_price)
                    return price
                else:
                    price = 0
                    max_pax_list = obj.paxwise_max_pax_list.split(',')
                    price_list = obj.paxwise_price_list.split(',')
                    # AND THEN CHECK HOW MANY PAX ARE REMAINING. FOR THEM FIND THE SMALLEST VEHICLE THAT CAN ACCOMMODATE REMAINING PAX.
                    # IF THE TOTAL NUMBER OF PAX IS MORE THAN THE MAXPAX OF BIGGEST VEHICLE, FIND HOW MANY MAXAPAX VEHICLES ARE REQUIRED,
                    maxpax_vehicles = total_pax // max_pax_list[-1]
                    remaining_pax = total_pax % max_pax_list[-1]
                    if maxpax_vehicles > 0:
                        price += maxpax_vehicles * price_list[-1]
                        for i in range(len(max_pax_list)):
                            if remaining_pax <= max_pax_list[i]:
                                price += price_list[i]
                                return price
                    else:
                        for i in range(len(max_pax_list)):
                            if total_pax <= max_pax_list[i]:
                                price += price_list[i]
                                return price
        return 'Pricing Error'
