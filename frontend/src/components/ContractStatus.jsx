const ContractStatus = (status) => {
  return (
    <>
      {status == 1 ? (
        <span className="badge text-bg-danger">Pending</span>
      ) : status == 2 ? (
        <span className="badge text-bg-warning">Processing..</span>
      ) : (
        <span className="badge text-bg-success">Processed</span>
      )}
    </>
  );
};

export default ContractStatus;
