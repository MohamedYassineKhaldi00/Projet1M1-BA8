from scrapy.exceptions import DropItem

class PipelineDeCleaning:
    # Expected fields
    expected_fields = [
        "titre", "url", "description", "niveau", "prerequis", 
        "credits_ects", "duree", "regime", "contenu", 
        "competences", "metiers", "secteurs", "modules", "secteur", "url", "metier"
    ]

    def process_item(self, item, spider):  # Change here
        # Clean and filter each object
        for field in self.expected_fields:
            value = item.get(field)

            # Clean strings and remove if 2 or fewer characters
            if isinstance(value, str):
                cleaned_value = value.replace("\n", "").replace("\t", "").strip()
                
                # Remove leading ": " if present
                if cleaned_value.startswith(": "):
                    cleaned_value = cleaned_value[2:]

                if len(cleaned_value) <= 2:
                    item.pop(field)  # Remove field if 2 or fewer characters
                else:
                    item[field] = cleaned_value

            # Clean lists and remove strings with 2 or fewer characters
            elif isinstance(value, list):
                cleaned_list = [
                    v.replace("\n", "").replace("\t", "").replace('"', "").replace("  ", " ").strip()
                    for v in value if isinstance(v, str) and len(v.strip()) > 2
                ]
                
                # Further clean each string in the list to remove leading ": "
                cleaned_list = [v[2:] if v.startswith(": ") else v for v in cleaned_list]
                
                # Remove the field if the list is empty after filtering
                if not cleaned_list:
                    item.pop(field)
                else:
                    item[field] = cleaned_list

        # Drop the item if all expected fields are empty
        if not any(field in item for field in self.expected_fields):
            raise DropItem(f"Dropping item with no valid fields: {item}")

        return item
