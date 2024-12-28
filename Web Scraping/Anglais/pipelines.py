from scrapy.exceptions import DropItem

class PipelineCleaning:
    expected_fields = [
        "Title", "url", "description", "Degree", "Prerequisite", 
        "Credits", "Duration", "Format", "contenu", 
        "Skills", "Careers", "Sectors", "Subjects", "Career_cluster", 
        "Career_pathway", "Occupation", "Tasks", "Technology_skills", 
        "Activities", "Knowledge", "Abilities", "Education", 
        "Interests", "Values", "Traits"
    ]

    def process_item(self, item, spider):
        def clean_string(value):
            """Cleans a single string value."""
            value = value.replace("\n", "").replace("\t", "").strip()
            return value[2:] if value.startswith(": ") else value

        def clean_list(value):
            """Cleans a list of string values."""
            return [
                clean_string(v) for v in value
                if isinstance(v, str) and len(v.strip()) > 2
            ]

        for field in self.expected_fields:
            value = item.get(field)

            if isinstance(value, str):
                cleaned_value = clean_string(value)
                if len(cleaned_value) > 2:
                    item[field] = cleaned_value
                else:
                    item.pop(field, None)

            elif isinstance(value, list):
                cleaned_list = clean_list(value)
                if cleaned_list:
                    item[field] = cleaned_list
                else:
                    item.pop(field, None)

        # Drop the item if all  fields  empty
        if not any(field in item for field in self.expected_fields):
            raise DropItem(f"Dropping item with no valid fields: {item}")

        return item