import yaml

class LocaleManager:
    locale_idx = 0
    fallback_idx = 0
    locale_dict = {}
    locale_names = []

    def getLocaleName(locale_idx : int):
        return LocaleManager.locale_names[locale_idx]

    def setLocale(locale_idx : int):
        # Set current locale by a given locale index according to the locale list(e.g. 0)
        LocaleManager.locale_idx = locale_idx

    def loadLocale(locale_name : str,  locale_dir : str):
        # Load locale strings from local file
        with open(locale_dir, "r", encoding="utf-8") as f:
            lang_str_dict = yaml.safe_load(f)
            LocaleManager.locale_dict[locale_name] = lang_str_dict

    def loadAllFromList(locale_list_dir : str):
        # Load all locales
        with open(locale_list_dir, "r", encoding="utf-8") as f:
            lang_dict = yaml.safe_load(f)
            for lang, lang_dir in lang_dict.items():
                LocaleManager.loadLocale(lang, lang_dir)
            LocaleManager.locale_names = list(LocaleManager.locale_dict.keys())

    def getAllNames():
        return LocaleManager.locale_names

    def getString(string_id : str):
        # Get string from the current locale
        try:
            return LocaleManager.locale_dict[LocaleManager.getLocaleName(LocaleManager.locale_idx)][string_id]
        except:
            return LocaleManager.locale_dict[LocaleManager.getLocaleName(LocaleManager.fallback_idx)][string_id]
        
    
    
