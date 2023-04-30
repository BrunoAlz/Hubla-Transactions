import Table from "../../components/ContractTable";
import Layout from "../Layout";
import { useDispatch, useSelector } from "react-redux";
import { useEffect } from "react";
import { contractTransactions } from "../../slices/contracts/contractsSlice";
import { useParams } from "react-router-dom";


const ContractsTransactions = () => {
  const { transactions } = useSelector((state) => state.contracts);
  const dispatch = useDispatch();
  const { contract_id } = useParams();

  useEffect(() => {
    dispatch(contractTransactions(contract_id));
  }, []);

  return (
    <div>
      <Layout />
      <div className="container-fluid">
        <div className="row">
          <main className="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <h1>Contracts</h1>
            {transactions ? <Table props={transactions} /> : "A"}
          </main>
        </div>
      </div>
    </div>
  );
};

export default ContractsTransactions;
