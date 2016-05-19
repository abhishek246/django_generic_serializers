Django Generic Serializer
=====================


**Generic** serializer for django model objects. It Serializes you model based on dict() that is passed as parameter to it.

----------


Documents
-------------

### Installation
Two ways to install using pip
```
	pip install django_generic_serializer
```
Build the repo manually 
```
	git clone https://github.com/abhishek246/django_generic_serializers.git
	cd django_generic_serializers
	python setup.py 
```


### Use Cases


```
	class Mymodel(models.Model):
		normal_field = models.CharField(max_length = 255)
		fk_field = models.ForeignKey(SomeModel, unique = True)
		m2m_field = models.ManyToManyField(OtherModel)

	class SomeModel(models.Model):
		some_field = models.CharField(max_length = 255)
	
	class OtherModel(models.Model):
		other_field = CharField(max_length = 255)
		other_field_two = models.DateTimeField(auto_now_add=True) 
```

You models should look similar to this
Importing Django Generic Serializer
```
	from django_generic_serializer import serializers
	serializer = serializers.Serializers()
	mymodel_object = Mymodel.objects.get(pk=1)
	res_dict = {
		'NormalField': 'normal_field',
		'some_field': 'fk_field.some_field',
		'm2m_field_data': {
			'field_name': 'm2m_field'
			'fields': {
				'otherField': 'other_field',
				'otherFieldTwo': 'other_field_two'
			}
		}
	}
```
