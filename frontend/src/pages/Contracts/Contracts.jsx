import ContractTable from "../../components/ContractTable";
import ContractForm from "../../components/ContractForm";
import Layout from "../Layout";
import { useDispatch, useSelector } from "react-redux";
import { useEffect } from "react";
import { contractsList } from "../../slices/contracts/contractsSlice";
import { toast } from "react-toastify";



const Contracts = () => {
  const { contracts, isLoading, isError, isSuccess, message } = useSelector(
    (state) => state.contracts
  );
  const dispatch = useDispatch();

  useEffect(() => {

    dispatch(contractsList());
  }, []);

  return (
    <div>
      <Layout />
      <div className="container-fluid">
        <div className="row">
          <main className="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <h1>Contracts</h1>
            {contracts ? <ContractTable props={contracts} /> : "A"}
          </main>
        </div>
      </div>
    </div>
  );
};

export default Contracts;
