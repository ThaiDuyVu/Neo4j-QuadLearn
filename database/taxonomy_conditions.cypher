// Chỉ cập nhật cạnh hiện có; không tạo node/cạnh hoặc sửa lịch sử học tập.
// condition_vi là điều kiện ĐỦ từ parent (tổng quát) thành child (đặc biệt).
// Áp dụng cho tứ giác lồi, không suy biến. Không liệt kê toàn bộ dấu hiệu nhận biết.
UNWIND [
  {child:'shape:square', parent:'shape:rectangle', condition:'Hai cạnh kề bằng nhau'},
  {child:'shape:square', parent:'shape:rhombus', condition:'Có một góc vuông'},
  {child:'shape:rectangle', parent:'shape:parallelogram', condition:'Có một góc vuông'},
  {child:'shape:rhombus', parent:'shape:parallelogram', condition:'Hai cạnh kề bằng nhau'},
  {child:'shape:parallelogram', parent:'shape:quadrilateral', condition:'Hai cặp cạnh đối song song'},
  {child:'shape:trapezoid', parent:'shape:quadrilateral', condition:'Chỉ một cặp cạnh đối song song'},
  {child:'shape:isosceles-trapezoid', parent:'shape:trapezoid', condition:'Hai góc kề một đáy bằng nhau'},
  {child:'shape:cyclic', parent:'shape:quadrilateral', condition:'Tổng hai góc đối bằng 180°'},
  {child:'shape:rectangle', parent:'shape:cyclic', condition:'Có hai góc kề bằng 90°'}
] AS item
MATCH (:Quadrilateral {id:item.child})-[r:IS_A]->(:Quadrilateral {id:item.parent})
SET r.condition_vi = item.condition
;
