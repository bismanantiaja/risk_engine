

class FraudHandler:
    import pandas as pd
    import numpy as np
    import json
    import pickle
    import datetime

    from shapely.geometry import Point
    from shapely.geometry.polygon import Polygon

    from geopandas import GeoDataFrame, points_from_xy
    import geopandas as gpd

    def __init__(self, data,mod_apps_filepath,daily_apps_filepath,indonesia_isp_filepath):
        self.data = data
        self.data = mod_apps_filepath
        
    def get_fraud_score(self):
        score = 0
        
        tmp_checks = self.fraud_checks()
        
        if tmp_checks['is_rooted'] == True:
            score += 10
        if tmp_checks['is_timezone_allowed'] == False:
            score += 80
        if tmp_checks['is_country_allowed'] == False:
            score += 80
        if tmp_checks['get_mod_apps_installed'] > 0:
            score += 80
        if tmp_checks['get_daily_apps_installed'] <= 2:
            score += 10
        if tmp_checks['is_isp_known'] == False:
            score += 10
        if tmp_checks['get_online_profiles_by_email'] <= 2:
            score += 10
        if tmp_checks['get_online_profiles_by_phone'] <= 2:
            score += 10
        if tmp_checks['get_online_profiles_others'] <= 1:
            score += 10
        if tmp_checks['is_ktp_digit_incorrect'] == True:
            score += 80
        if tmp_checks['is_email_domain_disposable'] == True:
            score += 80
        if tmp_checks['is_phone_activity_seen'] == False:
            score += 10
        if tmp_checks['is_phone_reachable'] == False:
            score += 10
        if tmp_checks['is_fraud_score_normal'] == False:
            score += 80
        
        return score
    
    def get_fraud_decision(self):
        score = self.get_fraud_score()
        
        if score >= 80:
            return 'DECLINED'
        else:
            return 'APPROVED'
        
        
    def fraud_checks(self):
        results = {
            'is_rooted': is_rooted(),
            'is_timezone_allowed': is_timezone_allowed(),
            'is_country_allowed': is_country_allowed(),
            'get_mod_apps_installed': get_mod_apps_installed(),
            'get_daily_apps_installed': get_daily_apps_installed(),
            'is_isp_known': is_isp_known(),
            'get_online_profiles_by_email': get_online_profiles_by_email(),
            'get_online_profiles_by_phone': get_online_profiles_by_phone(),
            'get_online_profiles_others': get_online_profiles_others(),
            'is_ktp_digit_incorrect': is_ktp_digit_incorrect(),
            'is_email_domain_disposable': is_email_domain_disposable(),
            'is_phone_activity_seen': is_phone_activity_seen(),
            'is_phone_reachable': is_phone_reachable(),
            'is_fraud_score_normal': is_fraud_score_normal(),
        }
        
        return results
    
    def get_online_profiles_by_email(self):
        iluma = self.data['advance']['iluma']
        
        count = 0
        
        if str(iluma['Facebook Email Registered']).lower() == 'true':
            count += 1
        if str(iluma['Instagram Email Registered']).lower() == 'true':
            count += 1
        if str(iluma['Microsoft Email Registered']).lower() == 'true':
            count += 1
        if str(iluma['Yahoo Email Registered']).lower() == 'true':
            count += 1
        if str(iluma['Twitter Email Registered']).lower() == 'true':
            count += 1
        if str(iluma['Twitter Email Registered']).lower() == 'true':
            count += 1
            
            
        return count
    
    def get_online_profiles_by_phone(self):
        iluma = self.data['advance']['iluma']
        
        count = 0
        
        if str(iluma['Facebook Phone Registered']).lower() == 'true':
            count += 1
        if str(iluma['Instagram Phone Registered']).lower() == 'true':
            count += 1
        if str(iluma['Microsoft Phone Registered']).lower() == 'true':
            count += 1
        if str(iluma['Yahoo Phone Registered']).lower() == 'true':
            count += 1
        if str(iluma['Twitter Phone Registered']).lower() == 'true':
            count += 1
        if str(iluma['Twitter Phone Registered']).lower() == 'true':
            count += 1
            
            
        return count
    
    def get_online_profiles_others(self):
        iluma = self.data['advance']['iluma']
        
        count = 0
        
        if str(iluma['WhatsApp Registered']).lower() == 'true':
            count += 1
        if str(iluma['Telegram Registered']).lower() == 'true':
            count += 1
        if str(iluma['AirBnB Registered']).lower() == 'true':
            count += 1
        if str(iluma['Booking.Com Registered']).lower() == 'true':
            count += 1
        if str(iluma['Spotify Registered']).lower() == 'true':
            count += 1
        if str(iluma['Amazon Registered']).lower() == 'true':
            count += 1
        if str(iluma['Ebay Registered']).lower() == 'true':
            count += 1
        if str(iluma['Apple Registered']).lower() == 'true':
            count += 1
        if str(iluma['Linkedin Registered']).lower() == 'true':
            count += 1
        if str(iluma['SnapChat Registered']).lower() == 'true':
            count += 1
        if str(iluma['Line Registered']).lower() == 'true':
            count += 1
            
        return count
    
    def is_phone_activity_seen():
        iluma = self.data['advance']['iluma']
        phone_activity = iluma['Recency of Activity']
        
        if phone_activity == 'not seen in the last 3 months':
            return False
        else:
            return True
        
    def is_phone_reachable():
        iluma = self.data['advance']['iluma']
        phone_status = iluma['Phone Status']
        
        if phone_status == 'Reachable':
            return True
        else:
            return False
        
    def is_fraud_score_normal():
        iluma = self.data['advance']['iluma']
        fraud_score = iluma['fraud_score']
        
        if fraud_score >= -2:
            return True
        else:
            return False
        
    
    def is_ktp_digit_incorrect():
        ktp = self.data['user']['ktp']
        
        if len(user['number']) <> 16:
            return True
        else:
            return False
        
    def is_email_domain_disposable():
        iluma = self.data['advance']['iluma']
        
        if str(iluma['Disposable Email']).lower() == 'true':
            return True
        else:
            return False
        
    
    def is_isp_known(self):
        isp = self.data['network']
        indonesia_isp = pd.read_csv(self.indonesia_isp_filepath)
        
        if isp['operator_name'].lower() in [isp.lower() for isp in indonesia_isp['isp_name']]:
            return True
        else:
            return False
    
    def get_mod_apps_installed(self):
        mod_apps_list = pd.read_csv(self.mod_apps_filepath)
        apps = self.data['phone_data']['app']['user_apps']
        
        count = 0
        
        for app in apps:
            packages = [package.lower() for packages in app.split('.')]
            for mod_app in mod_apps_list['app_name']:
                if str(mod_app) in packages:
                    count += 1
                
        return count
    
    def get_daily_apps_installed(self):
        daily_apps_list = pd.read_csv(self.daily_apps_filepath)
        apps = self.data['phone_data']['app']['user_apps']
        
        count = 0
        
        for app in apps:
            packages = [package.lower() for packages in app.split('.')]
            for daily_app in daily_apps_list['app_name']:
                if str(daily_app) in packages:
                    count += 1
                
        return count
                    
    
    def is_rooted(self):
        root = self.data['phone_data']['root']
        
        if str(root['is_rooted']) == 'false':
            return False
        else:
            return True
        
    def is_country_allowed(self, region):
        region = self.data['phone_data']['region']
        
        if region['country'] == 'ID':
            return True
        else:
            return False
        
    def is_timezone_allowed(self, region):
        region = self.data['phone_data']['region']
        
        if '+07' in str(region['timezone']) or '+08' in str(region['timezone']) or '+09' in str(region['timezone']):
            return True
        else:
            return False