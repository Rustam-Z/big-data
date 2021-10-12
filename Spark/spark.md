# Apache Spark

    Spark basics
    Spark SQL
    Spark ML
    Spark streaming


## Spark basics
    - Spark components, architecture, job scheduling process;
    - RDD, Pair RRD, shared variable;
    - ETL process;
    - APIs — RDDs, DataFrames, DataSets - benefits, performance, when to use;
    - Deployment models, cluster managers, web UI;
    - Catalyst optimizer - provides speed, concept of Spark SQL, CBO - Cost Based Optimizer;
    - Tungsten project - memory performance;

- [Spark introduction](#spark-introduction)
- [RDD and Operations](#rdd-and-operations)


### Spark introduction
- Spark Core - the heart of Apache Spark, core abstraction and processing engine. It provides the distributed task dispatching, scheduling, basic input and output operations, the RDD abstraction, and APIs to manipulate it.
- Spark - cluster computing framework with **in-memory** data processing
- MapReduce - on **disk-based** data processing (reading from cluster -> performing operations -> writing results back -> reading updated data -> operations -> write back)

#### Spark Driver
- One Driver ---> Set of Executors
- Driver Process:
    - Sits on the driver node (master node), hosts SparkContext for Spark application
    - Splits an application into tasks and schedules them to run on executors
    - Generates tasks across workers (using task scheduler)
    - Coordinates workers and overall execution of tasks
    - Maintaining information
    - Responding to user program
    - Analyzing
    - Distributing
    - Requires 
        - **ShuffleManager**
        - **MemoryManager** (execution memory = compting joins, sorts, aggregations; shared memory = for caching and spreading internal data across the nodes in a cluster)
        - **BroadcastManager** to manage broadcast variables 
- Executor process:
    - Reporting the state to driver node
    - Executing code
- Cluster manager
    - Controls physical machines
    - Allocate resources
    - YARN, Mesos, Kubernetes

#### Spark Context
- Heart of a Spark application 
- Sets internal services and connection to env
- After SparkContext is created, you can create RDDs, accumulators, and broadcast variables, access Spark services, and run jobs. (until `stop()`)
- Only one SparkContext per JVM (`spark.driver.allowMultipleContexts` just for testing purposes)
```scala
"""
SPARK CONTEXT
RDD Graph
DAG scheduler
Task scheduler
Scheduler backend
Listener bus
Block manager
"""
val sc = new SparkContext(master=("local[*]"),
  appName = "SparkContext Sample",
  new SparkConf)

val fileName = "people.csv"
val lines = sc.textFile(fileName)

val count = lines.count()
println(count)

sc.stop()
```

#### Spark Session
- Before Spark 2.0 there were SparkContext, StreamingContext, SqlContext (to connect to SparkSQL), and HiveContext (to interact with Hive stores). 
- After Spark 2.0 Datasets/DataFrames were introduced as distributed data abstraction interface. So it united all contexts. (+ unifies the different file format reading)
```scala
val ss = SparkSession.builder.master(master).appName(appName)
  .enableHiveSupport()
  .getOrCreate()
```

#### Spark Executor
- Executing code assigned to it by the driver 
- Reporting the computation state back to the driver node, report heartbeat too
- Identified with: `id` and `host` on which they run.
- Executors provide in-memory storage for RDDs cached in Spark applications 

#### Spark Architecture 
- Master/worker architecture
- Driver (master), executors (workers)
- Cluster manager is used to schedule the job in workers

#### Job Terms
- Job --> Stage --> Task --> (Compute RDD partition)
- Spark operates on **RDDs** (Resilient Distributed Dataset) - set of data spread across multiple machines
- A **Task**, also known as a command, is the smallest individual unit of execution launched to compute an RDD partition
- A **stage** is a set of parallel tasks - one task per partition. Like a layer of a neural network.
- A **Job** is a top-level execution for any Spark application, which corresponds to an action, and a driver program calls this action. The Job consists of a set of tasks arranged in stages.
    - Computing a job = computing the partitions of the RDD 
    - Job submission happens right after the action call


#### Directed Acyclic Graph
- In the DAG scheduling, the calculation process bases on the dependency between RDDs
    - Narrow dependencies (only one RDD will use the result of previous)
    - Wide dependencies (many RDD will use the result)

#### Job Scheduling Process
- RDD operations have two types: Transformations and Actions
    - **Transformations** = create a dataset from an existing one; function that produces new RDD from the existing ones
        - Transformations are *lazy*, meaning when you call some operation in RDD, it does not execute immediately
        - Since transformations are lazy, you can execute operations any time by calling an action on data
    - **Action** = return a value to the driver program after running a computation on the dataset
        - Actions are operations that trigger computation and return values
        - Spark Actions are RDD operations that produce non-RDD values
- What’s happening when it runs? First, create Spark Context and add an RDD. Then, after a list of transformations, you can get a DAG. Now, when an action is called, DAGScheduler performs its job. It splits the graph into stages of tasks and submits each one as ready. Afterward, DAGScheduler submits the taskSet to the TaskScheduler, and it does its job. The TaskScheduler launches tasks via cluster manager and retries failed or straggling tasks. The backend will receive the worker list from the Cluster Manager, and then it will launch Task at the Executor. A BlockManager at each Executor will help deal with shuffle data and cached RDDs. New TaskRunner is created at the Executor and it starts the thread pool to process the task set.

```scala
  val sc = new SparkContext(...)
  
  val rdd1 = "employees.csv"
  val rdd2 = "projects.scv"
  val result = rdd1.join(rdd2)
              .groupBy(...)
              .collect
```

### RDD and Operations
    Operations supported by Apache Spark;
    Abstractions RDD and Pair RRD;
    How Spark evaluates the code;
    Shared variable;

#### What is the RDD?
- RDDs are fault-tolerant, parallel data structures, that explicitly persist intermediate results in memory, and can be manipulated by the operations. They are *immutable, partitioned and distributed*
- **Resilient** = fault-tolerant with the help of RDD lineage graph and so able to recompute missing or damaged partitions due to node failures 
- **Distributed** with data residing on multiple nodes in a cluster
- **Dataset** = collection of partitioned data with primitive values


#### Partition
- Partition = logical chunk of a large data set
- Data can be separated into partitions among nodes
- 20 cores in cluster = 20 | 40 | 60 partitions
- Size = 128MB, and shuffle block <= 2GB
- Catalyst optimizer = determines the number and location of partition

#### **Transformations**
**Narrow transformation**
- Input and output stays in the same partition
- No data movement is needed
- Basic: `map(func)`, `filter(func)`, `union(func)`
    - `map()` = apply some func over source (rdd) `val z = sc.parallelize(1 to 3).map(i => i*i) // 1, 4, 9` 
    - `filter()` works same as in python (which elem returns true) `val z = sc.parallelize(1 to 3).filter(i => i % 2 == 1) // 1, 3`
    - `union()` = combines two RDDs
        ```
        val x = sc.parallelize(1 to 3)
        val y = sc.parallelize(3 to 5)
        val z = x.union(y)
        // 1, 2, 3, 3, 4, 5
        ```
- Mapping transformations: 
    - `flatMap(func), mapPartitions(), mapPartitionsWithIndex()`
    - `mapPartitions` = similar to map but runs separately on each partition (block) of the RDD
    - `mapPartitionsWithIndex` = similar to mapPartitions. However, it provides func with an integer value representing the index of the partition
- Zipping transformations:
    - Zips this RDD with another one, returns key-value pairs (PairRDD)
    - `zip(dataset), zipWithIndex(), zipWithUniqueID()`
    -
        ```
        val x = sc.parallelize('A' to 'C',2)
        val y = sc.parallelize(1 to 3, 2)
        val z = x.zip(y)
        // (A,1), (B,2), (C,3)
        ```
    - 
        ```
        val x = sc.parallelize('A' to 'C',2)
        val z = x.zipWithIndex()
        // (A,0), (B,1), (C,2)
        ```
    -
        ```
        // Items in the kth partition will get ids k, n+k, 2*n+k
        val x = sc.parallelize('A' to 'C',2)
        val z = x.zipWithUniqueId()
        // (A,0), (B,1), (C,3)
        ```
**Wide transformation**
- Input from other partitions are required
- **Data shuffling** is needed before processing, data is shuffled between nodes means (repartitioning)

- `intersection(dataset)` - returns a new RDD that contains the intersection of elements

- `distinct([numTasks])` - returns a new dataset that contains the distinct elements

- `groupByKey([numTasks])`

- `reduceByKey(func, [numTasks])`

- `sortByKey([ascending], [numTasks])`

- `join(dataset, [num])`

- `coalesce(numTasks)` - ONLY decreases the number of partitions

- `repartition(numTasks)` - can change the number of partitions, increase or decrease. Remember that repartitioning does not mean equal value distribution. It is just a repartitioning, even if you get empty partitions.

- `cartesian(dataset)`
```
val x = sc.parallelize(1 to 5)
val y = sc.parallelize(3 to 6, 2)
val z = x.intersection(y)
// 4, 3, 5
```
```
val x = sc.parallelize(Array(1, 2, 1, 3, 2), 2)
val z = x.distinct()
// 1, 3, 2
```
```
val x = sc.parallelize(1 to 6, 4)
// [1], [2, 3], [4], [5, 6]

val z = x.coalesce(2)
// [1, 2, 3], [4, 5, 6]
```

#### **Actions**
> count(); collect(); take(n); top(n); countByValue(); reduce(func); fold(zeroValue, func); aggregate(zeroValue, seqOp, combOp); foreach(func); saveAsTextFile(path); saveAsSequenceFile(path); saveAsObjectFile(path)
- `take(n)` = takes `n` elements starting from zero partition
- `top(n)` = takes n elements in unordered way. `val x = sc.parallelize(1 to 5).top(3)`
- For data aggregation: reduce, fold, aggregate 
- `reduce(func)` = aggregate the data 
    - `val x = sc.parallelize(1 to 4).reduce((acc, item) => acc + item)// 10` // 1+2+3+4=10
- `fold(zeroValue, func)` =  same as reduce, but you can add default values
    - `val x = sc.parallelize(1 to 4).filter(_>10).fold(0)((acc, item) => acc + item) // 0`
- `aggregate(zeroValue, seqOp, combOp)` - default values, aggregates the elements with `seqOp`, then the results for all the partitions with `combOp` 
#### How it works together?
```scala
import org.apache.spark.{SparkConf, SparkContext}

object WordCount {
    def main(args: Array[String]): Unit = {
        val conf = new SparkConf().setAppName("Word Count").setMaster("local[*]")
        val sc = new SparkContext(conf)

        // Create RDD
        val textFile = sc.textFile(args(0))

        // Run all the transformations you have
        val counts = textFile.flatMap(line => line.split(" "))
            .map(word => (word, 1))
            .reduceByKey(_ + _)

        // Spark runs the action "saveAsTextFile"
        counts.saveAsTextFile(args(1))
    }
}
```

#### Lazy Evaluation
- Spark maintains the lineage of transformations but does not immediately evaluate until an action is called
- Only when the action is performed, Spark finally estimates all the previous steps skipped for that RDD

#### PairRDD
- https://www.oreilly.com/library/view/learning-spark/9781449359034/ch04.html
- RDDs containing key/value pairs
- pairRDD operations are applied on each key/value in parallel && regroup data in network
-  Basic transformations `mapValues(func), flatMapValues(func), keys, values`
    - `mapValues(func)` = applies func to each value 
    - `flatMapValues(func)` = apply a function that returns an iterator to each value of a pair RDD, and for each element returned, produce a key/value entry with the old key. Often used for tokenization.
    ```
    P(1, 2), (3, 4), (3, 6)} 

    rdd.mapValues(x => x+1) // {(1, 3), (3, 5), (3, 7)}

    rdd.flatMapValues(x => (x to 5) // {(1, 2), (1, 3), (1, 4), (1, 5), (3, 4), (3, 5)}

    rdd.keys() // {1, 3, 3}
    rdd.values() // {2, 4, 6}

    rdd.reduceByKey((x, y) => x + y) // {(1, 2), (3, 10)}
    rdd.groupByKey() // {(1, [2]), (3, [4, 6])}

    Array((‘B', 1), ('B', 2), (‘A', 3) , (‘A’, 4) , (‘B’, 5))
    
    rdd.aggregateByKey((0, 0))( // (zeroValue, seqOp, combOp)
        (acc, item) => (acc._1 + item, acc._2 + 1),
        (acc1,acc2) => (acc1._1 + acc2._1, acc1._2 + acc2._2)) // (B,(8,3)), (A,(7,2))

    rdd.sortByKey // // (A,3), (A,4), (B,1), (B,2), (B,5)
    ```

#### Two PairRDD Transformations
- `subtractByKey` remove elements with a key present in the other RDD
- `cogroup` groups data from both RDDs sharing the same key (groupWith)
- `join` = inner join between two RDDs
    - (K, V) & (K, W) ==> (K, (V, W)) with all pairs 
    - `leftOuterJoin`, `rightOuterJoin`, and `fullOuterJoin`.

```scala
val x = sc.parallelize(Array(('C', 1), ('B', 2), ('A', 3), ('A', 4)))
val y = sc.parallelize(Array(('A', 8), ('B', 7), ('A', 6), ('D', 5)))

val z = x.subtractByKey(y) // (C,1)

val z = x.cogroup(y) // (B,([2],[7])), (A,([3, 4],[8, 6])), (C,([1],[])), (D,([],[5]))

val z1 = x.join(y)
val z2 = x.leftOuterJoin(y)
val z3 = x.rightOuterJoin(y)
```

#### Actions on PairRDD
- `countByKey` = count number of elements for each key
- `collectAsMap` = collect result as a map to provide easy lookup
- `lookup` = returns all values associated with the provided key

```scala
{(1, 2), (3, 4), (3, 6)}

rdd.countByKey()  // {(1, 1), (3, 2)}
rdd.collectAsMap() // Map{(1, 2), (3, 4), (3, 6)}
rdd.lookup(3) // [4, 6]
```

#### Shuffle
- **Shuffling** is a process of redistributing data across partitions = **repartitioning**, move data between JVM processes or executors with wire
- Shuffling is the process of data transfer between stages
- By default, it doesn’t change the number of partitions, but their content
- repartition and coalesce , ByKey operations (except for counting) like groupByKey and reduceByKey, and join operations like cogroup and join.
- groupByKey change to reduceByKey

#### Shared Variables
- Function (map or reduce) passed, variables are copied to each machine, and no updates come back to driver program. 
- Broadcast variables, accumulators 

#### Accumulators
- can be used to to implement counters (as in MapReduce) or sums 
- native support for numeric types, extensions possible via API
- workers (transformation) can modify, but cannot read
- only a driver (action) can read the accumulated value

#### Broadcast
- allow programmers to keep a read-only variable cached on each machine rather than shipping its copy with tasks
- allow for an efficient sharing of potentially large data sets
- workers have read-only access
- useful for reference data lookups

## Links
- Tuning Spark: ttp://spark.apache.org/docs/latest/tuning.html#level-of-parallelism
- Transformations and actions: https://www.slideshare.net/SparkSummit/transformations-and-actions-a-visual-guide-training
- Examples (filter, map, reduce, groupBy, combineByKey, flatMap ...): https://backtobazics.com/category/big-data/spark/
- RDD Programming guide, Spark docs: https://spark.apache.org/docs/latest/rdd-programming-guide.html