# Decision Tree Induction ID3
ID3 Decision Tree Induction for nominal data sets. The output is an easily viewable XML tree.

### Dependinces
```
pip install numpy
```



### CSV Example: Playing Baseball
| Outlook  | Temperature | Humidity | Windy | Play ball | 
|----------|-------------|----------|-------|-----------| 
| Rainy    | Hot         | High     | False | No        | 
| Rainy    | Hot         | High     | True  | No        | 
| Overcast | Hot         | High     | False | Yes       | 
| Sunny    | Mild        | High     | False | Yes       | 
| Sunny    | Cool        | Normal   | False | Yes       | 
| Sunny    | Cool        | Normal   | True  | No        | 
| Overcast | Cool        | Normal   | True  | Yes       | 
| Rainy    | Mild        | High     | False | No        | 
| Rainy    | Cool        | Normal   | False | Yes       | 
| Sunny    | Mild        | Normal   | False | Yes       | 
| Rainy    | Mild        | Normal   | True  | Yes       | 
| Overcast | Mild        | High     | True  | Yes       | 
| Overcast | Hot         | Normal   | False | Yes       | 
| Sunny    | Mild        | High     | True  | No        | 


### Output: Induced ID3 Tree
```
<?xml version="1.0" ?>
<ID3 column_split="Outlook" gain="0.2467">
	<Rainy column_split="Humidity" gain="0.971">
		<High Entropy="1.0">
			<No type="SOLUTION"/>
		</High>
		<Normal Entropy="1.0">
			<Yes type="SOLUTION"/>
		</Normal>
	</Rainy>
	<Overcast Entropy="1.0">
		<Yes type="SOLUTION"/>
	</Overcast>
	<Sunny column_split="Windy" gain="0.971">
		<False Entropy="1.0">
			<Yes type="SOLUTION"/>
		</False>
		<True Entropy="1.0">
			<No type="SOLUTION"/>
		</True>
	</Sunny>
</ID3>

```
Where tag 'column-split' points at to the next column to look at and the name of each element is the nominal value.


### Future Work
Currently, this program only generates a tree, however future implimentation will include a method to test the tree on a testing dataset






