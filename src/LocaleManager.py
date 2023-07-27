import yaml

class LocaleManager:
    locale = "zh-cn"
    fallback = "zh-cn"
    locale_dict = {}

    def setLocale(locale_id : str):
        # Set current locale to a locale identifier (e.g. zh-cn)
        LocaleManager.locale = locale_id

    def loadLocale(locale_id : str,  locale_dir : str):
        # Load locale strings from local file
        with open(locale_dir, "r", encoding="utf-8") as f:
            lang_str_dict = yaml.safe_load(f)
            LocaleManager.locale_dict[locale_id] = lang_str_dict

    def loadAllFromList(locale_list_dir : str):
        # Load all locales
        with open(locale_list_dir, "r", encoding="utf-8") as f:
            lang_dict = yaml.safe_load(f)
            for lang, lang_dir in lang_dict.items():
                LocaleManager.loadLocale(lang, lang_dir)

    def getString(string_id : str):
        # Get string from the current locale
        try:
            return LocaleManager.locale_dict[LocaleManager.locale][string_id]
        except:
            return LocaleManager.locale_dict[LocaleManager.fallback][string_id]
        
    def getAllLocales():
        return list(LocaleManager.locale_dict.keys())
