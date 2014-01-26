<?php
// Create connection
$con=mysqli_connect("db501482795.db.1and1.com","dbo501482795","mtolive5","db501482795");

// Check connection
if (mysqli_connect_errno($con))
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }

$result = mysqli_query($con,"SELECT count(*) as c FROM articles");
while($row = mysqli_fetch_array($result))
  {
  echo "Total records: ".$row['c'];
  }

$result = mysqli_query($con,"SELECT * FROM logs ORDER BY date DESC");
echo "<table>";
  echo "<tr><td>Date</td>";
  echo "<td>Num Inserted</td>";
  echo "<td>Num Error</td>";
  echo "<td>Num Found</td>";
  echo "</tr>";
while($row = mysqli_fetch_array($result))
  {

  echo "<tr><td>".$row['date']."</td>";
  echo "<td>" . $row['num_inserted']."</td>";
  echo "<td>" . $row['num_error']."</td>";
  echo "<td>" . $row['num_found']."</td>";
  echo "</tr>";
  }

 echo "</table>";
mysqli_close($con);
?> 